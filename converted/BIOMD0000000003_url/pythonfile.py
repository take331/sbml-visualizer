import sbmltoodepy.modelclasses
from scipy.integrate import odeint
import numpy as np
import operator
import math

class ModelName(sbmltoodepy.modelclasses.Model):

	def __init__(self):

		self.p = {} #Dictionary of model parameters
		self.p['V1'] = sbmltoodepy.modelclasses.Parameter(None, 'V1', False, metadata = sbmltoodepy.modelclasses.SBMLMetadata("V1"))
		self.p['V3'] = sbmltoodepy.modelclasses.Parameter(None, 'V3', False, metadata = sbmltoodepy.modelclasses.SBMLMetadata("V3"))
		self.p['VM1'] = sbmltoodepy.modelclasses.Parameter(3.0, 'VM1', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata("VM1"))
		self.p['VM3'] = sbmltoodepy.modelclasses.Parameter(1.0, 'VM3', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata("VM3"))
		self.p['Kc'] = sbmltoodepy.modelclasses.Parameter(0.5, 'Kc', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata("Kc"))

		self.c = {} #Dictionary of compartments
		self.c['cell'] = sbmltoodepy.modelclasses.Compartment(1.0, 3, True, metadata = sbmltoodepy.modelclasses.SBMLMetadata("cell"))

		self.s = {} #Dictionary of chemical species
		self.s['C'] = sbmltoodepy.modelclasses.Species(0.01, 'Concentration', self.c['cell'], False, constant = False, metadata = sbmltoodepy.modelclasses.SBMLMetadata("Cyclin"))
		self.s['M'] = sbmltoodepy.modelclasses.Species(0.01, 'Concentration', self.c['cell'], False, constant = False, metadata = sbmltoodepy.modelclasses.SBMLMetadata("CDC-2 Kinase"))
		self.s['X'] = sbmltoodepy.modelclasses.Species(0.01, 'Concentration', self.c['cell'], False, constant = False, metadata = sbmltoodepy.modelclasses.SBMLMetadata("Cyclin Protease"))

		self.r = {} #Dictionary of reactions
		self.r['reaction1'] = reaction1(self)
		self.r['reaction2'] = reaction2(self)
		self.r['reaction3'] = reaction3(self)
		self.r['reaction4'] = reaction4(self)
		self.r['reaction5'] = reaction5(self)
		self.r['reaction6'] = reaction6(self)
		self.r['reaction7'] = reaction7(self)

		self.f = {} #Dictionary of function definitions
		self.time = 0

		self.AssignmentRules()



	def AssignmentRules(self):

		self.p['V1'].value = self.s['C'].concentration * self.p['VM1'].value * (self.s['C'].concentration + self.p['Kc'].value)**-1

		self.p['V3'].value = self.s['M'].concentration * self.p['VM3'].value

		return

	def _SolveReactions(self, y, t):

		self.time = t
		self.s['C'].amount, self.s['M'].amount, self.s['X'].amount = y
		self.AssignmentRules()

		rateRuleVector = np.array([ 0, 0, 0], dtype = np.float64)

		stoichiometricMatrix = np.array([[ 1,-1,-1,0,0,0,0.],[ 0,0,0,1,-1,0,0.],[ 0,0,0,0,0,1,-1.]], dtype = np.float64)

		reactionVelocities = np.array([self.r['reaction1'](), self.r['reaction2'](), self.r['reaction3'](), self.r['reaction4'](), self.r['reaction5'](), self.r['reaction6'](), self.r['reaction7']()], dtype = np.float64)

		rateOfSpeciesChange = stoichiometricMatrix @ reactionVelocities + rateRuleVector

		return rateOfSpeciesChange

	def RunSimulation(self, deltaT, absoluteTolerance = 1e-12, relativeTolerance = 1e-6):

		finalTime = self.time + deltaT
		y0 = np.array([self.s['C'].amount, self.s['M'].amount, self.s['X'].amount], dtype = np.float64)
		self.s['C'].amount, self.s['M'].amount, self.s['X'].amount = odeint(self._SolveReactions, y0, [self.time, finalTime], atol = absoluteTolerance, rtol = relativeTolerance, mxstep=5000000)[-1]
		self.time = finalTime
		self.AssignmentRules()

class reaction1:

	def __init__(self, parent, metadata = None):

		self.parent = parent
		self.p = {}
		if metadata:
			self.metadata = metadata
		else:
			self.metadata = sbmltoodepy.modelclasses.SBMLMetadata("creation of cyclin")
		self.p['vi'] = sbmltoodepy.modelclasses.Parameter(0.025, 'vi')

	def __call__(self):
		return self.parent.c['cell'].size * self.p['vi'].value

class reaction2:

	def __init__(self, parent, metadata = None):

		self.parent = parent
		self.p = {}
		if metadata:
			self.metadata = metadata
		else:
			self.metadata = sbmltoodepy.modelclasses.SBMLMetadata("default degradation of cyclin")
		self.p['kd'] = sbmltoodepy.modelclasses.Parameter(0.01, 'kd')

	def __call__(self):
		return self.parent.s['C'].concentration * self.parent.c['cell'].size * self.p['kd'].value

class reaction3:

	def __init__(self, parent, metadata = None):

		self.parent = parent
		self.p = {}
		if metadata:
			self.metadata = metadata
		else:
			self.metadata = sbmltoodepy.modelclasses.SBMLMetadata("cdc2 kinase triggered degration of cyclin")
		self.p['vd'] = sbmltoodepy.modelclasses.Parameter(0.25, 'vd')
		self.p['Kd'] = sbmltoodepy.modelclasses.Parameter(0.02, 'Kd')

	def __call__(self):
		return self.parent.s['C'].concentration * self.parent.c['cell'].size * self.p['vd'].value * self.parent.s['X'].concentration * (self.parent.s['C'].concentration + self.p['Kd'].value)**-1

class reaction4:

	def __init__(self, parent, metadata = None):

		self.parent = parent
		self.p = {}
		if metadata:
			self.metadata = metadata
		else:
			self.metadata = sbmltoodepy.modelclasses.SBMLMetadata("activation of cdc2 kinase")
		self.p['K1'] = sbmltoodepy.modelclasses.Parameter(0.005, 'K1')

	def __call__(self):
		return self.parent.c['cell'].size * (1 + -1 * self.parent.s['M'].concentration) * self.parent.p['V1'].value * (self.p['K1'].value + -1 * self.parent.s['M'].concentration + 1)**-1

class reaction5:

	def __init__(self, parent, metadata = None):

		self.parent = parent
		self.p = {}
		if metadata:
			self.metadata = metadata
		else:
			self.metadata = sbmltoodepy.modelclasses.SBMLMetadata("deactivation of cdc2 kinase")
		self.p['V2'] = sbmltoodepy.modelclasses.Parameter(1.5, 'V2')
		self.p['K2'] = sbmltoodepy.modelclasses.Parameter(0.005, 'K2')

	def __call__(self):
		return self.parent.c['cell'].size * self.parent.s['M'].concentration * self.p['V2'].value * (self.p['K2'].value + self.parent.s['M'].concentration)**-1

class reaction6:

	def __init__(self, parent, metadata = None):

		self.parent = parent
		self.p = {}
		if metadata:
			self.metadata = metadata
		else:
			self.metadata = sbmltoodepy.modelclasses.SBMLMetadata("activation of cyclin protease")
		self.p['K3'] = sbmltoodepy.modelclasses.Parameter(0.005, 'K3')

	def __call__(self):
		return self.parent.c['cell'].size * self.parent.p['V3'].value * (1 + -1 * self.parent.s['X'].concentration) * (self.p['K3'].value + -1 * self.parent.s['X'].concentration + 1)**-1

class reaction7:

	def __init__(self, parent, metadata = None):

		self.parent = parent
		self.p = {}
		if metadata:
			self.metadata = metadata
		else:
			self.metadata = sbmltoodepy.modelclasses.SBMLMetadata("deactivation of cyclin protease")
		self.p['K4'] = sbmltoodepy.modelclasses.Parameter(0.005, 'K4')
		self.p['V4'] = sbmltoodepy.modelclasses.Parameter(0.5, 'V4')

	def __call__(self):
		return self.parent.c['cell'].size * self.p['V4'].value * self.parent.s['X'].concentration * (self.p['K4'].value + self.parent.s['X'].concentration)**-1


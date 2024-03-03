import sbmltoodepy.modelclasses
from scipy.integrate import odeint
import numpy as np
import operator
import math

class ModelName(sbmltoodepy.modelclasses.Model):

	def __init__(self):

		self.p = {} #Dictionary of model parameters
		self.p['Kd'] = sbmltoodepy.modelclasses.Parameter(1e-05, 'Kd', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))
		self.p['Ksp'] = sbmltoodepy.modelclasses.Parameter(0.001, 'Ksp', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))
		self.p['dspksp'] = sbmltoodepy.modelclasses.Parameter(None, 'dspksp', False, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))
		self.p['dspspkd'] = sbmltoodepy.modelclasses.Parameter(None, 'dspspkd', False, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))
		self.p['h'] = sbmltoodepy.modelclasses.Parameter(2.0, 'h', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))
		self.p['k0'] = sbmltoodepy.modelclasses.Parameter(0.1, 'k0', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))
		self.p['ka'] = sbmltoodepy.modelclasses.Parameter(40.0, 'ka', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))
		self.p['ks'] = sbmltoodepy.modelclasses.Parameter(10.0, 'ks', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))
		self.p['ku'] = sbmltoodepy.modelclasses.Parameter(0.1, 'ku', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))
		self.p['s'] = sbmltoodepy.modelclasses.Parameter(1000.0, 's', True, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))

		self.c = {} #Dictionary of compartments
		self.c['univ'] = sbmltoodepy.modelclasses.Compartment(1.0, 3, True, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))

		self.s = {} #Dictionary of chemical species
		self.s['P'] = sbmltoodepy.modelclasses.Species(10.0, 'Amount', self.c['univ'], False, constant = False, metadata = sbmltoodepy.modelclasses.SBMLMetadata(""))

		self.r = {} #Dictionary of reactions
		self.r['___r1'] = ___r1(self)
		self.r['___r2'] = ___r2(self)

		self.f = {} #Dictionary of function definitions
		self.time = 0

		self.AssignmentRules()



	def AssignmentRules(self):

		self.p['dspksp'].value = (self.p['Ksp'].value / 2) * (1 + (self.p['s'].value + self.s['P'].concentration * self.c['univ'].size) / self.p['Ksp'].value - ((1 + (self.p['s'].value + self.s['P'].concentration * self.c['univ'].size) / self.p['Ksp'].value)**2 - 4 * self.p['s'].value * self.s['P'].concentration * self.c['univ'].size / self.p['Ksp'].value**2)**0.5)

		self.p['dspspkd'].value = (self.p['Kd'].value / 2) * (1 + 2 * self.p['dspksp'].value / self.p['Kd'].value - ((1 + 2 * self.p['dspksp'].value / self.p['Kd'].value)**2 - 4 * self.p['dspksp'].value**2 / self.p['Kd'].value**2)**0.5)

		return

	def _SolveReactions(self, y, t):

		self.time = t
		self.s['P'].amount = y
		self.AssignmentRules()

		rateRuleVector = np.array([ 0], dtype = np.float64)

		stoichiometricMatrix = np.array([[ 1,-1.]], dtype = np.float64)

		reactionVelocities = np.array([self.r['___r1'](), self.r['___r2']()], dtype = np.float64)

		rateOfSpeciesChange = stoichiometricMatrix @ reactionVelocities + rateRuleVector

		return rateOfSpeciesChange

	def RunSimulation(self, deltaT, absoluteTolerance = 1e-12, relativeTolerance = 1e-6):

		finalTime = self.time + deltaT
		y0 = np.array([self.s['P'].amount], dtype = np.float64)
		self.s['P'].amount = odeint(self._SolveReactions, y0, [self.time, finalTime], atol = absoluteTolerance, rtol = relativeTolerance, mxstep=5000000)[-1]
		self.time = finalTime
		self.AssignmentRules()

class ___r1:

	def __init__(self, parent, metadata = None):

		self.parent = parent
		self.p = {}
		if metadata:
			self.metadata = metadata
		else:
			self.metadata = sbmltoodepy.modelclasses.SBMLMetadata("")

	def __call__(self):
		return self.parent.p['ks'].value * (self.parent.p['k0'].value + (self.parent.p['dspspkd'].value / self.parent.p['ka'].value)**self.parent.p['h'].value) / (1 + (self.parent.p['dspspkd'].value / self.parent.p['ka'].value)**self.parent.p['h'].value)

class ___r2:

	def __init__(self, parent, metadata = None):

		self.parent = parent
		self.p = {}
		if metadata:
			self.metadata = metadata
		else:
			self.metadata = sbmltoodepy.modelclasses.SBMLMetadata("")
		self.p['__RATE__'] = sbmltoodepy.modelclasses.Parameter(0.1, '__RATE__')

	def __call__(self):
		return self.p['__RATE__'].value * self.parent.s['P'].concentration


# 生物学的プロセスに関する可視化アプリケーションの開発

## 背景(なぜやるのか)
システム生物学における数理モデルは、生物学的プロセスやシステムの動態を表現し、理解を深めるためのツールとして重要である。

これらのモデルは数学的な方程式やネットワーク構造で表現され、シミュレーションや解析によって、生物学的プロセスの探求を可能にする。
しかし、これらの数理モデルのみで、反応のダイナミクスを理解することは困難である。

## 目的(何を達成するのか)
- 既存のアプリケーションには存在しない機能の実装  
- 非専門家でも扱いやすい  
- 科学的発見の可能性を向上させる
- より多くの人が理解できる形で表現する

## 方法(どうやって達成するか)
### BioModelsについて
モデルの開発は、データ科学者と実験科学者の分析において、ますます一般的かつ重要なツールになっているため、異なるユーザのコミュニティない及び、コミュニティ間でモデルの共有ｔ再利用を可能にすることから重要になっている。 

数理モデルの有用な共有と交換を促進するために必要な最初のステップは、数理モデルをエンコードできる標準的な手段であり、これはモデルをエンコードするための機械可読な言語である「SBML」や「CellML」によって達成された。

そして、これらのモデルを保存、及び共有するためのリポジトリが「BioModels」である。

BioModelsは2006年に作成された生物学的に興味深い定量的モデルを保存、交換、取得するための無料オープンソースリポジトリである。  

BioModelsは２つの主要なブランチで構成されており、モデルが表現しようとしている生物学的プロセスへの対応と、対応する査読済み出版物に記載されているシミュレーション結果の再現性の両方を検証するために、大規模なモデルのセットが厳選されている。  

1. 文献に由来するモデルで構成されたブランチ
2. 自動プロセスを通じて生成されたブランチ


下図が示すように、2014年時点で1200を超えるモデルに加え、経路リソースから自動的に生成された140,000oを超えるモデルをホストしている。  
BioModelsへのモデル送信料は年々増加しており、これは同時にモデリング分野の拡大を示している。


![m_gku1181fig1](https://github.com/take331/sbml-visualizer/assets/73569757/45e4467a-f062-4f3c-a8fb-e2b7ff48e96c)

Systems Biology Format Converter (SBFC)は、SBMLモデルを複数のモデリング言語やプログラミング言語のスクリプトに変換するためのツール群である(Rodriguez et al., 2016)。  
BioModels Databaseは、SBFCを使用して、SBMLモデルの大規模なライブラリを、ユーザーがダウンロードできる他の形式に自動変換している（

### Systems Biology Markup Language (SBML)
SBMLは生物学的プロセスの計算モデルを通信及び保存するための、XMLに基づく表現形式である  

SBMLは代謝ネットワーク、細胞シグナル伝達経路、制御ネットワーク感染症などを含む、様々な種類の生物学的現象を表すことができる

SBMLには、おおきく３つの目的がある  
- すべてのツールの特異なファイル形式に準拠するようにモデルを書き直すことなく、複数のソフトウェアツールを使用できるようにする
- 異なるソフトウェア環境で作業している場合でも他の研究者が使用できる形式でモデルを共有及び公開できるようにする
- モデルの作成に使用されたソフトウェアの寿命を超えてモデルが確実に存続するようにする

以上より、SBMLの目的は、計算モデルの重要な側面を伝達するために現在の様々なソフトウェアツールで使用される交換形式である共通語として機能することである。 

### SBMLtoODEpy
SBMLtoODEpyはSBMLモデルをPythonクラスに変換するソフトウェアパッケージである  
これは、Pythonで記述された生物医学システムに迅速に組み込んだり、直接シミュレートして使用することが出来る

SBMLtoODEpyによって、Pythonのクラスを使用するコードを生成し、独自のコードを書いてインターフェースを作成する

### lib
#### PySimpleGUI 

## Todo
- [x] SBMLファイルの変換
  - [x] inputs_modelフォルダ内のファイルを表示
  - [x] Browseボタンから、任意のSBMLファイルを選択
- [ ] 数式の表示
- [ ] テーブルの作成
- [ ] ネットワーク図
- [ ] アニメーションの実装

### Small Tasks
- [ ] 画面の最大化＆高画質化

## Usage
1. SBMLファイルのダウンロード  
  [BioModels](https://www.ebi.ac.uk/biomodels/)からSBMLファイルをダウンロードする  
  ダウンロードしたファイルはinputs_model内または、任意のディレクトリから参照することが可能

2. モデルの可視化  
   Importボタンをクリックして、SBMLファイルを変換する  
   変換したファイルは、プログラムに対応していくつかの機能によって可視化される

3. パラメータの変更
   パラメータを変更して、再度可視化を行う

4. 保存
   結果を様々な形式で保存する

## References
- [BioModels](https://www.ebi.ac.uk/biomodels/)
- [BioModels Database: An enhanced, reated nd annotated resource for published quantitative](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2909940/)
- [BioModels ten-year anniversary](https://academic.oup.com/nar/article/43/D1/D542/2439069)
- [SBMLtoODEpy](https://github.com/AnabelSMRuggiero/sbmltoodepy)
- [Modeling formalisms in Systems Biology](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3285092/)
- [Systems Biology: A Brief Overview](https://www.science.org/doi/10.1126/science.1069492?url_ver=Z39.88-2003&rfr_id=ori:rid:crossref.org&rfr_dat=cr_pub%20%200pubmed)
- [From functional genomics to systems biology: concepts and practices](https://www.sciencedirect.com/science/article/pii/S1631069103002300)

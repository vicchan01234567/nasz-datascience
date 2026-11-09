# 2. óra – Gépi tanulás a Titanic-adatsoron

A házi feladatban modelleket és hiperparamétereket vizsgáltam, a tanuló- és tesztpontosság alapján értékelve a teljesítményt és a túlillesztést. A megoldásomban döntési fákat és Random Foresteket próbáltam ki.

## Órai viszonyítási alap

| Modell | Tesztpontosság |
|---|---:|
| Logisztikus regresszió | 77,1% |
| SVM | 82,5% |
| Döntési fa | 82,1% |
| Random Forest | 82,1% |
| Gradient Boosting | 84,3% |
| Neurális háló | 79,8% |

## Megoldásom

A `Survived` oszlopot célnak, a `Pclass`, `Sex`, `Age`, `SibSp`, `Parch` és `Embarked` mezőket bemenetnek használtam. A `PassengerId`, `Name`, `Ticket`, `Cabin` és `Fare` oszlopokat kihagytam, hogy az első kísérletet az alapjellemzőkre szűkítsem.

Kipróbáltam a hiányzó értékek leginkább hasonló utastól való pótlását, de ez egyelőre zsákutcának bizonyult. A modellek a hiányzó értékeket a tanítóadatok mediánjával vagy leggyakoribb kategóriájával pótolták.

Három Gini-alapú döntési fát tanítottam külön-külön, rétegzett, véletlen 80/20-as felosztásokon. A `min_samples_leaf=0` érvénytelen, ezért az első modellnél 1-et használtam. Mivel a felosztások eltérnek, az eredmények nem közvetlenül összehasonlíthatók.

| Módszer | Beállítások | Tanuló pontosság | Tesztpontosság |
|---|---|---:|---:|
| Döntési fa, Gini | `max_depth=21`, `min_samples_leaf=1` (0 helyett) | 93,4% | 80,3% |
| Döntési fa, Gini | `max_depth=15`, `min_samples_leaf=5` | 86,7% | 83,1% |
| Döntési fa, Gini | `max_depth=10`, `min_samples_leaf=10` | 85,7% | 77,0% |

## Eredmények

- **21-es mélység:** [ábra](./decision_tree_depth21_leaf1.png) · [jelentés](./decision_tree_depth21_leaf1.txt) · [modell](./decision_tree_depth21_leaf1_model.joblib) · [előrejelzések](./decision_tree_depth21_leaf1_predictions.csv)
- **15-ös mélység:** [ábra](./decision_tree_depth15_leaf5.png) · [jelentés](./decision_tree_depth15_leaf5.txt) · [modell](./decision_tree_depth15_leaf5_model.joblib) · [előrejelzések](./decision_tree_depth15_leaf5_predictions.csv)
- **10-es mélység:** [ábra](./decision_tree_depth10_leaf10.png) · [jelentés](./decision_tree_depth10_leaf10.txt) · [modell](./decision_tree_depth10_leaf10_model.joblib) · [előrejelzések](./decision_tree_depth10_leaf10_predictions.csv)
- [Kísérletek összefoglalója](./decision_tree_comparison.txt)

## Források

- [2. házi feladat leírása](https://github.com/karpatika92/nasz_data_science_course/blob/master/lessons/02-gepi-tanulas/homework.md)
- [Órai modellek viszonyítási alapja](https://github.com/csepimarci/-Marci--data-science-kurzus/blob/main/2.%20ora/homework.md#%C3%B3rai-modellek-viszony%C3%ADt%C3%A1si-alapja)

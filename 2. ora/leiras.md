# 2. óra – Gépi tanulás a Titanic-adatsoron

A házi feladat második részében két modellt és legalább három-három hiperparaméter-beállítást kellett kipróbálnom, majd a tanuló- és tesztpontosság alapján értékelnem a túlillesztést. A megoldásomban a döntési fákra és random forestekre összpontosítottam.

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

A `Survived` oszlopot célnak, a `Pclass`, `Sex`, `Age`, `SibSp`, `Parch` és `Embarked` oszlopokat bemenetnek használtam. A `PassengerId`, `Name`, `Ticket`, `Cabin` és `Fare` mezőket az egyszerűbb, alapjellemzőkre szűkített első modell kedvéért hagytam el.

Kipróbáltam a hiányzó értékek leginkább hasonló utastól való pótlását, de ezt egyelőre zsákutcának bizonyult. Ehelyett a hiányzó értékeket a modellek a tanítóadatok mediánjával vagy leggyakoribb kategóriájával pótolták.

Mindkét Gini-alapú döntési fát rétegzett, véletlen 80/20-as felosztással tanítottam és teszteltem. (A két modell különböző felosztása miatt az eredmények csak tájékoztató jelleggel hasonlíthatók össze.)

| Módszer | Beállítások | Pontosság |
|---|---|---:|
| Döntési fa, Gini | `max_depth=21`, `min_samples_leaf=1` | 80,3% |
| Döntési fa, Gini | `max_depth=15`, `min_samples_leaf=5` | 83,1% |

### Eredmények

- [21 mélységű fa ábrája](./decision_tree_depth21_leaf1.png) · [részletek](./decision_tree_depth21_leaf1.txt) · [modell](./decision_tree_depth21_leaf1_model.joblib) · [tesztelőrejelzések](./decision_tree_depth21_leaf1_predictions.csv)
- [15 mélységű fa ábrája](./decision_tree_depth15_leaf5.png) · [részletek](./decision_tree_depth15_leaf5.txt) · [modell](./decision_tree_depth15_leaf5_model.joblib) · [tesztelőrejelzések](./decision_tree_depth15_leaf5_predictions.csv)
- [Kísérletek összefoglalója](./decision_tree_comparison.txt)

## Források

- [2. házi feladat leírása](https://github.com/karpatika92/nasz_data_science_course/blob/master/lessons/02-gepi-tanulas/homework.md)
- [Órai modellek viszonyítási alapja](https://github.com/csepimarci/-Marci--data-science-kurzus/blob/main/2.%20ora/homework.md#%C3%B3rai-modellek-viszony%C3%ADt%C3%A1si-alapja)

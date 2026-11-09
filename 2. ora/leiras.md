# 2. óra – Gépi tanulás a Titanic-adatsoron

## A házi feladat második része: hiperparaméter-vadászat

A házi feladat második részében azt a feladatot kaptam, hogy a Titanic-adatsoron kipróbált modellek teljesítményét hiperparaméterek változtatásával javítsam. Két modellt kellett választanom a hat vizsgált modellcsaládból, majd mindkettőnél legalább három különböző beállítást kipróbálnom. Minden esetben külön kellett rögzítenem a tanuló- és tesztpontosságot, mert a nagy különbség túlillesztésre utalhat. Ezután értékelnem kellett, melyik beállítás teljesített a legjobban, és melyik mutatott túlillesztést. Bónuszként egy további, például K legközelebbi szomszéd (KNN) modellt is kipróbálhattam volna, kitérve a dimenzióátok hatására.

A teljes feladatleírást a [Gépi tanulás – 2. házi feladat](https://github.com/karpatika92/nasz_data_science_course/blob/master/lessons/02-gepi-tanulas/homework.md) oldalon olvashatom.

## Órai modellek viszonyítási alapja

Az alábbi tesztpontosságokat az [órai modellek viszonyítási alapja](https://github.com/csepimarci/-Marci--data-science-kurzus/blob/main/2.%20ora/homework.md#%C3%B3rai-modellek-viszony%C3%ADt%C3%A1si-alapja) táblázatából vettem.

| Modell | Tesztpontosság |
|---|---:|
| Logisztikus regresszió | 77,1% |
| SVM | 82,5% |
| Döntési fa | 82,1% |
| Random Forest | 82,1% |
| Gradient Boosting | 84,3% |
| Neurális háló | 79,8% |

## Amit az adatokkal és a modellekkel végeztem

A Titanic-adatsorban a `Survived` oszlopot használtam célváltozóként, a `Pclass`, `Sex`, `Age`, `SibSp`, `Parch` és `Embarked` mezőket pedig bemenetként. A `PassengerId` oszlopot azért hagytam el, mert csupán az utas azonosítója. A `Name`, `Ticket`, `Cabin` és `Fare` mezőket is kihagytam, hogy az első kísérletet az alapvető utasjellemzőkre szűkítsem; nem azért, mert ezek általában haszontalanok lennének.

Kipróbáltam a hiányzó értékek pótlását is úgy, hogy minden hiányzó mezőnél a többi oszlop alapján leginkább hasonló utas megfelelő adatát másoltam át. Végül ezt a módszert zsákutcának tekintettem, és nem használtam a modellekhez, mert a hasonlóság meghatározásakor a túlélési címke is bekerülhetett volna, ami adatszivárgást okozhat. Az eredeti, szűrt CSV-ben meghagytam a hiányzó adatokat; a modelljeim a hiányzó számértékeket a tanítóadatok mediánjával, a kategóriákat pedig a tanítóadatok leggyakoribb értékével pótolták.

Két Gini-impuritást használó döntési fát tanítottam a 891 soros adathalmaz rétegzett, véletlen 80/20-as felosztásán. Az első modellnél 21-re állítottam a maximális mélységet. A kért `min_samples_leaf=0` értéket a scikit-learn nem engedi meg, ezért a legkisebb érvényes értéket, az 1-et használtam. A 42-es véletlenmaggal kapott tesztpontosságom 80,3% lett. A második modellt 15-ös maximális mélységgel és 5-ös minimális levélmérettel tanítottam, a 43-as véletlenmaggal végzett teszten 83,1%-os pontosságot értem el.

A két modellhez különböző véletlen felosztást használtam, ezért a tesztpontosságaik nem hasonlíthatók össze teljesen közvetlenül: az eltérést a modellbeállítások mellett a tesztutasok különbsége is befolyásolhatta. Mindkét fám gyökércsomópontja a `Sex_female <= 0.5` feltétellel választja szét a nemeket.

## Az elkészült fáim és eredményeim

### 21-es mélység, minimális levélméret 1

- [Döntési fám ábrája](./decision_tree_depth21_leaf1.png)
- [A Gini-értékek és ágak szöveges leírása](./decision_tree_depth21_leaf1.txt)
- [DOT-faábra](./decision_tree_depth21_leaf1.dot)
- [Betanított modellem](./decision_tree_depth21_leaf1_model.joblib)
- [Tesztutasokra adott előrejelzéseim](./decision_tree_depth21_leaf1_predictions.csv)

### 15-ös mélység, minimális levélméret 5

- [Döntési fám ábrája](./decision_tree_depth15_leaf5.png)
- [A Gini-értékek és ágak szöveges leírása](./decision_tree_depth15_leaf5.txt)
- [DOT-faábra](./decision_tree_depth15_leaf5.dot)
- [Betanított modellem](./decision_tree_depth15_leaf5_model.joblib)
- [Tesztutasokra adott előrejelzéseim](./decision_tree_depth15_leaf5_predictions.csv)

- [A két kísérletem összefoglalója](./decision_tree_comparison.txt)

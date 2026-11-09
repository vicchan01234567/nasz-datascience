# 2. óra – Gépi tanulás a Titanic-adatsoron

## A házi feladat második része: hiperparaméter-vadászat

A gyakorlati feladat célja, hogy a Titanic-adatsoron kipróbált modellek teljesítményét hiperparaméterek változtatásával javítsuk. Két modellt kell választani a hat vizsgált modellcsaládból, majd mindkettőnél legalább három különböző beállítást kipróbálni. Minden esetben külön kell rögzíteni a tanuló- és tesztpontosságot: a nagy különbség túlillesztésre utalhat. Röviden értékelni kell, melyik beállítás teljesített a legjobban, és melyik mutatott túlillesztést. Bónuszként egy további, például K legközelebbi szomszéd (KNN) modell is vizsgálható, kitérve a dimenzióátok hatására.

A teljes feladatleírás a [Gépi tanulás – 2. házi feladat](https://github.com/karpatika92/nasz_data_science_course/blob/master/lessons/02-gepi-tanulas/homework.md) oldalon olvasható.

## Órai modellek viszonyítási alapja

Az alábbi tesztpontosságok az [órai modellek viszonyítási alapja](https://github.com/csepimarci/-Marci--data-science-kurzus/blob/main/2.%20ora/homework.md#%C3%B3rai-modellek-viszony%C3%ADt%C3%A1si-alapja) táblázatából származnak.

| Modell | Tesztpontosság |
|---|---:|
| Logisztikus regresszió | 77,1% |
| SVM | 82,5% |
| Döntési fa | 82,1% |
| Random Forest | 82,1% |
| Gradient Boosting | 84,3% |
| Neurális háló | 79,8% |

## Amit az adatokkal és a modellekkel végeztünk

A Titanic-adatsorban a `Survived` oszlopot használtuk célváltozóként, a `Pclass`, `Sex`, `Age`, `SibSp`, `Parch` és `Embarked` mezőket pedig bemenetként. A `PassengerId` oszlopot azért hagytuk el, mert csupán az utas azonosítója; a `Name`, `Ticket`, `Cabin` és `Fare` mezőket pedig kihagytuk, hogy az első kísérletet a kiválasztott alapvető utasjellemzőkre szűkítsük, nem azért, mert ezek általában haszontalanok lennének.

Kipróbáltuk a hiányzó értékek pótlását is úgy, hogy minden hiányhoz a többi mező alapján leginkább hasonló utas megfelelő adatát másoltuk át. Ezt a módszert végül nem használtuk a modellekhez, mert a hasonlóság meghatározásakor a túlélési címke is bekerülhetett volna, ami adatszivárgást okozhat. Az eredeti, szűrt CSV-ben meghagytuk a hiányzó adatokat, a modellek pedig a hiányzó számértékeket a tanítóadatok mediánjával, a kategóriákat pedig a tanítóadatok leggyakoribb értékével pótolták.

Két Gini-impuritást használó döntési fát tanítottunk a 891 soros adathalmaz rétegzett, véletlen 80/20-as felosztásán. Az első modell 21-es maximális mélységet kapott. A kért `min_samples_leaf=0` értéket a scikit-learn nem engedi meg, ezért a legkisebb érvényes értéket, az 1-et használtuk; a 42-es véletlenmaggal kapott tesztpontosság 80,3% lett. A második modell 15-ös maximális mélységgel és 5-ös minimális levélmérettel készült, a 43-as véletlenmaggal végzett teszten 83,1%-os pontosságot ért el.

A két modell különböző véletlen felosztást kapott, ezért a tesztpontosságaik nem teljesen közvetlenül összehasonlíthatók: az eltérés a modellbeállítások mellett a tesztutasok különbségéből is eredhet. Mindkét fa gyökércsomópontja a `Sex_female <= 0.5` feltétellel választja szét a nemeket.

## Az elkészült fák és eredmények

### 21-es mélység, minimális levélméret 1

- [Döntési fa ábrája](./decision_tree_depth21_leaf1.png)
- [Gini-értékek és ágak szöveges leírása](./decision_tree_depth21_leaf1.txt)
- [DOT-faábra](./decision_tree_depth21_leaf1.dot)
- [Betanított modell](./decision_tree_depth21_leaf1_model.joblib)
- [Tesztutasok előrejelzései](./decision_tree_depth21_leaf1_predictions.csv)

### 15-ös mélység, minimális levélméret 5

- [Döntési fa ábrája](./decision_tree_depth15_leaf5.png)
- [Gini-értékek és ágak szöveges leírása](./decision_tree_depth15_leaf5.txt)
- [DOT-faábra](./decision_tree_depth15_leaf5.dot)
- [Betanított modell](./decision_tree_depth15_leaf5_model.joblib)
- [Tesztutasok előrejelzései](./decision_tree_depth15_leaf5_predictions.csv)

- [A két kísérlet összefoglalója](./decision_tree_comparison.txt)

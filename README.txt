HNEFLTAFL
Michal Doneberk

Pravidla
- Všechny postavy mohou táhnout libovolný počet volných polí nahoru, dolů, doleva a doprava, dokud nenarazí na překážku.
- Na pole v rohu hracího plánu smí vstoupit jen král.
- Každá postava je zajata, pokud je ze dvou protilehlých stran sevřena nepřáteli (Pokud kámen do této pozice vstoupí, zajat není)
- Hra končí zajetím krále nebo jeho útěkem přes roh herní plochy

Ovládání
"Which side are you playing as? (Attacker(A)/Defender(B))"
"Which side plays first? (Attacker(A)/Defender(B))"
- Hra očekává pouze velké A nebo B, bez znaku konce řádku

"Starting point: "
"Ending point: "
- Hra očekává malé písmeno (a až "šířka herní plochy") mezeru a číslo (a až "výška herní plochy")

Struktura kódu
1.Import and variables
2.Setting-up functions
3.Tiles and their interaction
4.Finding valid moves
5.AI
6.Player
7.Gameplay
8.Running the game
9.End

1.Obsahuje globální proměnné a importovaný random pro náhodné určení stejně duležitých pohybů pro počítač
2.Načítá z textových souborů hrací plochu, zaplní herní plochu vzájemně lineárně spojenými "Poli",určuje kdo hraje jakou stranu a prvního hráče
3.Obsahuje třídu "Pole", funkce na zajatí postav a funkce na pohyb (funguje přepsáním cíle: A->B je B=A,A=" ")
4.Funkce na hledání vhodných možností pohybu
5.Obsahuje funkce na určování tahu a upravování priority tahů počítače (počítač vybírá náhodný tah s nejvyšší prioritou, priritu zvyšuje zajetí nepřítele, možnost vyhodit krále...) 
6.Obsahuje tah hráče a kontroli vhodného tahu
7.Obsahuje zobrazování herní plochy a jednotlivé tahy
8.Funkce v provozu, samotný herní cyklus s podmínkami na konec hry
9.KOnec hry
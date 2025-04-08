# Sieni-tunnistus
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen julkaisuja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään julkaisuja.
* Käyttäjä näkee sovellukseen lisätyt julkaisut. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät julkaisut.
* Käyttäjä pystyy etsimään julkaisuja hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään, että muiden käyttäjien lisäämiä julkaisuja.
* Käyttäjä pystyy kommentoimaan omia ja muiden käyttäjien julkaisuja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan omia kommenttejaa.
* Käyttäjä pystyy lisäämään kuvia julkaisuunsa, sekä poistamaan niitä.
* Sovelluksessa on käyttäjä sivut, jotka näyttävät tilastoja ja käyttäjän julkaisut.
* Käyttäjä pystyy valitsemaan julkaisuunsa luokisuksen (esim. tunnistus, reseptit, vapaa jne.)

## Sovelluksen asennus

Asenna `flask` -kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut

```
$ sqlite3 database.db < schema.sql
```

Voit käynnystää sovelluksen näin:

```
$ flask run
```

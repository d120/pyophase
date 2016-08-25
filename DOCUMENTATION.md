# pyophase: User-Dokumentation


## Admin-Bereich und Dashboard

Unter `/admin` ist der Admin-Bereich erreichbar, der die Verwaltung sämtlicher Django-Modelle (bzw. Objekte) erlaubt (also die eigentlichen gespeicherten Daten). Dort können Objekte erzeugt, verändert oder gelöscht werden. Für manche Modelle sind bestimmte Admin-Aktionen definiert, die weitere Funktionalität auf ausgewählten Objekten bieten. Diese werden unten an passender Stelle erwähnt.

Unter `/dashboard` befindet sich das Dashboard, welches neben ein paar informativen Widgets Zugang zu erweiterten Funktionen bietet, die im Admin-Bereich nicht gut zu realisieren wären. Auch diese Funktionen werden unten an passender Stelle genannt.

Der Admin-Bereich und das Dashboard sind zugangsgeschützt. Die Leitung kann im Admin-Bereich unter *Benutzer* Accounts für Organisatoren anlegen und mit bestimmten Rechten ausstatten. Je mehr Rechte an den Account gebunden sind, desto mehr Funktionalitäten stehen im Admin-Bereich und im Dashboard zur Verfügung.


## Ophasen

Im Admin-Bereich unter *Ophasen* kann ein neues Ophase-Objekt angelegt werden. Genau eine Ophase kann zeitgleich aktiv geschaltet sein. Das bedeutet, dass neue Objekte, die beispielsweise über das Mitmachen-Formular erzeugt werden, automatisch dieser Ophase zugeordnet werden. Das Erstellen einer Ophase ist also erforderlich bevor weitere Schritte unternommen werden können.

Ist eine Ophase vorrüber und werden die angefallenen Daten nicht mehr benötigt, sollte die alte Ophase gelöscht werden. Da die ausschließlich für diese Ophase relevanten Objekte diese Ophase referenzieren, werden sie automatisch mitgelöscht. Dies verhindert die unangemessene Vorhaltung von Daten.


## Personalverwaltung

Eine zentrale Komponente von pyophase ist die Verwaltung der beteiligten Personen, also Tutoren, Helfer und Orgas. Bevor diese sich über das **Mitmachen-Formular** registrieren können, sind ein paar Schritte im **Admin-Bereich** zu erledigen:
* Unter *Gruppenkategorien* werden die Arten von Kleingruppen definiert (Bachelor, Master Grundständig, ...)
* Unter *Orgajobs* werden die Jobs definiert, für die Organisatoren benötigt werden
* Unter *Helferjobs* werden die Jobs definiert, für die Helfer benötigt werden
* Unter *Kleidergrößen* werden die Kleidergrößen für das Ophasen-Kleidungsstück definiert, die zur Auswahl stehen
* Unter *Einstellungen* kann nun feingranular eingestellt werden, für welche Art Personal die Registrierung geöffnet ist

Im **Dashboard** unter *Personal* ist es möglich:
* Mehrere Kleingruppen auf einmal zu erstellen
* Die Tutoren auf Kleingruppen zu verteilen

Im Admin-Bereich stehen für *Personen* einige **Admin-Aktionen** zur Verfügung:
* *E-Mail Mass Subscription Export* erstellt eine Liste im Format `Vorname Nachname <email@adresse>` die als Input für einen Mailinglisten-Mass-Import genutzt werden kann
* *Übersicht exportieren* erzeugt eine Datei mit den wichtigsten Daten und Tätigkeitsfeldern der Personen
* *Helfer-Übersicht anzeigen* zeigt übersichtlich welcher Helfer sich für welche Aufgaben interessiert
* *Kleidergrößenübersicht* zeigt eine Zuordnung von Kleidergröße zu Personen

Um den Input für die **Namensschilder**-Erzeugungsapplikation zu generieren stehen für *Personen* und *Kleingruppen* die Admin-Aktionen *Namensschilderexport* und *Kleingruppen exportieren* zur Verfügung.


## Erstie-Verwaltung

Während der Ophase können sich die Erstsemester registrieren um sich für die Ophasenklausur oder für Newsletter anzumelden. Damit die Eintragung über das Formular funktioniert müssen zuerst ein paar Schritte im **Admin-Bereich** unternommen werden:
* Unter *Newsletter* die zur Auswahl stehenden Newsletter einstellen
* Unter *Einstellungen* die Registrierung aktivieren oder deaktivieren

Das Registrierungsformular ist zugangsgeschützt um Spaß-Einträgen vorzubeugen. Es kann etwa ein Tutor-Account angelegt werden, der dann auf den Rechnern benutzt wird, an denen sich die Erstsemester eintragen sollen.

Im **Dashboard** unter *Ersties* ist es möglich:
* Den aktuellen Eintragungsstand nach Kleingruppe einzusehen
* Den LaTeX-Code für die Ophasenscheine zu exportieren
* Den Eintragungsstand für die Newsletter einzusehen und für den Mailinglisten-Mass-Import zu exportieren

## Ophasenklausur

pyophase hilft bei der Organisation der Ophasenklausur. Im **Admin-Bereich** müssen dazu zunächst unter *Klausurräume* die zur Verfügung stehenden Räume konfiguriert werden.

Im **Dashboard** ist es dann möglich:
* eine automatische Zuteilung von Erstsemestern auf Klausurräume zu veranlassen
* die Anwesenheitsliste für die Klausurräume zu exportieren

## Workshops

Auch Angebote für Workshops können über pyophase gesammelt werden. Im **Admin-Bereich** müssen zunächst die zur Verfügung stehenden Zeitslots angelegt und die Registrierung in den Einstellungen freigeschaltet werden. Danach ist das Einreichen von Workshops über das Frontend möglich.

# MWQuest

## Wo ist die Seite für die Einstellungen?

Die [Seite für die Spielereinstellungen dieses Spiels](../player-options) enthält alle Optionen die man benötigt, um
eine YAML-Datei zu konfigurieren und zu exportieren.

## Was ist MWQuest?

MWQuest ist ein Spiel, welches von NewSoupVi für Archipelago entwickelt wurde.  
Es ist ein minimalistisches 8bit-inspiriertes Abenteuerspiel mit gitterförmiger Bewegungssteuerung.  
MWQuest ist ungefähr 20 Sekunden lang. Der Client kann aber nahtlos zwischen mehreren MWQuest-Slots wechseln.
Wenn du 10 MWQuest-Slots in einer Multiworld haben willst, sollte das also problemlos möglich sein.if you want to have 10 of them, that should work pretty well.

Ausschlaggebend ist bei MWQuest, dass das gesamte Spiel in der .apworld enthalten ist.  
Wenn du also die .apworld in deine 
[Archipelago-Installation](https://github.com/ArchipelagoMW/Archipelago/releases/latest) installiert hast,
kannst du MWQuest spielen.

## Warum existiert MWQuest?

MWQuest ist als Beispiel-.apworld geschrieben, mit welchem neue .apworld-Entwickler lernen können, wie man eine
.apworld schreibt.  
Der [MWQuest-Quellcode](https://github.com/NewSoupVi/Archipelago/tree/mwquest/worlds/mwquest) enthält unzählige Kommentare und Beispiele, die erklären,
wie jeder Teil der World-API funktioniert.  
Dabei nutzt er nur die modernsten API-Funktionen (Stand: 2025-08-24).

Das sekundäre Ziel von MWQuest ist, eine semi-minimale, generische .apworld zu sein, die Archipelago selbst gehört.  
Damit kann sie für Archipelagos Unit-Tests benutzt werden,
ohne dass sich die Archipelago-Entwickler davor fürchten müssen, dass MWQuest irgendwann gelöscht wird.

Das dritte Ziel von MWQuest ist, das erste "Spiel in einer .apworld" zu sein,
wobei das ganze Spiel in Python und Kivy programmiert ist
und innerhalb seines CommonClient-basierten Clients spielbar ist.  
Ich bin mir nicht ganz sicher, dass es wirklich das erste Spiel dieser Art ist, aber ich kenne bis jetzt keine anderen.

## Wenn ich mich im MWQuest-Client angemeldet habe, wie spiele ich dann das Spiel?

WASD oder Pfeiltasten zum Bewegen.  
Leertaste, um dein Schwert zu schwingen (wenn du es hast) und um mit Objekten zu interagieren.  
C, um die Konfettikanone zu feuern.

Öffne Kisten, zerhacke Büsche, öffne Türen, aktiviere Knöpfe, besiege Gegner.  
Sobald du den Drachen im oberen rechten Raum bezwingst, gewinnst du das Spiel.  
Das ist alles! Viel Spaß!

## Ein Statement zum Besitz von MWQuest

MWQuest ist mit der [MIT-Lizenz](https://opensource.org/license/mit) lizenziert,  
was heißt, dass es von jedem für jeden Zweck modifiziert und verbreitet werden kann.  
Archipelago hat jedoch seine eigenen Besitztumsstrukturen, die über der MIT-Lizenz stehen.  
Diese Strukturen machen es unklar,
ob eine .apworld-Implementierung überhaupt permanent verlässlich in Archipelago bleibt.

Im Zusammenhang mit diesen unverbindlichen, nicht gesetzlich verpflichtenden Besitztumsstrukturen
mache ich die folgende Aussage.

Ich, NewSoupVi, verzichte hiermit auf alle Rechte, MWQuest aus Archipelago zu entfernen.  
Dies bezieht sich auf alle Teile von MWQuest mit der Ausnahme der Musik und der Soundeffekte.  
Wenn ich die Töne entfernt haben möchte, muss ich dafür selbst einen PR öffnen.  
Dieser PR darf nur die Töne entfernen und muss MWQuest intakt und spielbar halten.

Solang ich der Maintainer von MWQuest bin, möchte ich als solcher agieren.  
Das heißt, dass jegliche Änderungen an MWQuest zuerst von mir genehmigt werden müssen.

Wenn ich jedoch aufhöre, der Maintainer von MWQuest zu sein,
egal ob es mein eigener Wunsch war oder ich meinen Maintainer-Verantwortungen nicht mehr nachkomme,
dann wird MWQuest automatisch Eigentum der Core-Maintainer von Archipelago,
die dann frei entscheiden können, was mit MWQuest passieren soll.  
Es wäre mein Wunsch, dass wenn MWQuest an eine andere Einzelperson übergeben wird,
diese Person sich an ähnliche Eigentumsregelungen hält wie ich.

Hoffentlich stellt dieses Statement sicher, dass MWQuest für immer eine .apworld sein kann,
auf die Archipelago sich verlassen kann.  
Wenn die Besitztumsstrukturen von Archipelago geändert werden,
vertraue ich den Core-Maintainern (bzw. den Eigentümern von Archipelago generell) damit,
angemessene Entscheidungen darüber zu treffen,
wie dieses Statement im Kontext der neuen Regeln interpretiert werden sollte.

# PPC Project: At the Crossroads

Jean-Baptiste SIMON / Hugo NOEL

## Introduction

Ce projet de simulation de trafic à une intersection a été développé dans le cadre du cours de Programmation Parallèle et Concurrente. L'objectif principal est de modéliser et de gérer le flux de véhicules normaux et prioritaires à une intersection en utilisant des techniques de programmation vues en cours de PPC.

La simulation doit permettre de visualiser en temps réel l'état des feux de circulation, le nombre de véhicules en attente dans chaque direction, et de s'assurer que les véhicules prioritaires peuvent traverser l'intersection en toute sécurité.

## Conception, choix techniques, architecture et protocoles d’échanges

### Choix du langage et des bibliothèques

Nous avons utilisé Python pour implémenter ce projet.

- Bibliothèques nécessaires pour répondre aux consignes : `multiprocessing`, `threading`, `socket`, `signal`
- Bibliothèques utilisées en plus par nous : `pygame`, `time`, `json`, `os`

### Choix de l'architecture

L'architecture du projet est basée sur plusieurs processus et threads.

Il y a 4 processus principaux :

- **normal_traffic_gen** : Génère le trafic de véhicules normaux
- **priority_traffic_gen** : Génère le trafic de véhicules prioritaires
- **lights** : Gère les feux de circulation
- **coordinator** : Gère le passage des véhicules en fonction des feux de circulation et des véhicules prioritaires

Le serveur est géré par un thread, qui ouvre un nouveau thread pour gérer chaque client qui se connecte.

### Protocoles d’échange

- **Queues** : Les files d’attente sont utilisées pour stocker les véhicules en attente de traverser l’intersection. Il y a une file d’attente pour chaque direction (nord, sud, est, ouest). Elles sont implémentées à l’aide de la classe Queue du module multiprocessing. Les véhicules sont ajoutés à la file d’attente correspondant à leur direction de provenance, et retirés lorsqu’ils traversent l’intersection.
- **Shared Memory** : La mémoire partagée est utilisée pour stocker l’état des feux de circulation et le nombre de véhicules dans chaque direction. Elle est implémentée à l’aide de la classe Array du module multiprocessing. L'état des feux de circulation est stocké dans un tableau partagé (TRAFFIC_LIGHTS), où chaque élément représente l'état d'un feu (vert ou rouge) et le temps restant avant le changement de feux. Le nombre de véhicules dans chaque direction est également stocké dans un tableau partagé (BOUCHONS).
- **Signals** : Les signaux sont utilisés pour indiquer la présence de véhicules prioritaires sur les différentes directions de l’intersection. Ils sont implémentés à l’aide de la classe Event du module multiprocessing. Chaque direction à son propre signal. Lorsqu’un véhicule prioritaire est détecté, le signal correspondant est activé. Il est désactivé une fois que le véhicule a traversé l’intersection.
- **Sockets** : Les sockets sont utilisés pour la communication entre le serveur d'affichage et les clients. Ils permettent d'envoyer des mises à jour en temps réel sur l'état de l'intersection aux clients connectés. Les sockets sont implémentés à l'aide du module socket. Le serveur d'affichage crée un socket serveur qui écoute les connexions entrantes des clients. Les clients créent des sockets clients qui se connectent au serveur. Les messages sont envoyés et reçus via les sockets.

## Pseudo-code des algorithmes importants

### Génération de trafic normal et prioritaire

```python
'Queues', 'Sirenes': Nord, Sud, Est, Ouest
def normal_traffic:
    Répéter indéfiniment:
        Attendre un temps de génération aléatoire
        Créer un véhicule : 'id' paire, 'type' normal, 'source' et
            'destination', 't_pass')
        Ajouter le véhicule dans la queue de provenance
def priority_traffic:
    Répéter indéfiniment:
        normal_traffic(); 'id' impaire, 'type' priority, 't_pass'
        Activer la sirène de la queue de provenance
```

### Gestion des feux

```python
't_feux' = temps avant inversion des feux
def lights_manager:
    Répéter indéfiniment:
        Si sirène activée -> nord:
            Ajuster les feux pour permettre le passage du véhicule
                prioritaire -> nord
            Attendre que le véhicule prioritaire passe
            Réinitialiser les feux pour le trafic normal (Est/Ouest
                vert)
        Si sirène activée -> sud:
            Ajuster les feux pour permettre le passage du véhicule
                prioritaire -> sud
            Attendre que le véhicule prioritaire passe
            Réinitialiser les feux pour le trafic normal (Est/Ouest
                vert)
        Si sirène activée -> est:
            Ajuster les feux pour permettre le passage du véhicule
                prioritaire -> est
            Attendre que le véhicule prioritaire passe
            Réinitialiser les feux pour le trafic normal (Nord/Sud vert)
        Si sirène activée -> ouest:
            Ajuster les feux pour permettre le passage du véhicule
                prioritaire -> ouest
            Attendre que le véhicule prioritaire passe
            Réinitialiser les feux pour le trafic normal (Nord/Sud
                vert)
        Si temps de switch atteint:
            Inverser les feux pour le trafic normal
        Attendre 1 seconde
        Décrémenter le temps restant avant le prochain switch de feux
```

### Coordination des véhicules

```python
def coordinator_process:
    Répéter indéfiniment:
        Si feu vert -> nord et file nord non vide:
            Permettre au véhicule de passer
            Réduire le nombre de véhicules en attente -> nord
            Supprimer le véhicule de la liste des véhicules
            Attendre le temps de passage du véhicule
        Si feu vert -> sud et file sud non vide:
            Permettre au véhicule de passer
            Réduire le nombre de véhicules en attente -> sud
            Supprimer le véhicule de la liste des véhicules
            Attendre le temps de passage du véhicule
        Si feu vert -> est et file est non vide:
            Permettre au véhicule de passer
            Réduire le nombre de véhicules en attente -> est
            Supprimer le véhicule de la liste des véhicules
            Attendre le temps de passage du véhicule
        Si feu vert -> ouest et file ouest non vide:
            Permettre au véhicule de passer
            Réduire le nombre de véhicules en attente -> ouest
            Supprimer le véhicule de la liste des véhicules
            Attendre le temps de passage du véhicule
        Attendre un court instant avant de vérifier à nouveau
```

## Plan d’implantation et tests effectués

### Plan d'implantation

1. Implémentation des processus individuels : Chaque processus (génération de trafic normal, génération de trafic prioritaire, gestion des feux, coordination) a été implémenté et testé individuellement avec des données codées en dur.
2. Implémentation de la communication inter-processus : Les communications entre les processus ont été implémentées et testées par paires.
3. Intégration des processus : Tous les processus ont été intégrés et testés ensemble.
4. Implémentation du serveur d'affichage : Le serveur d'affichage a été implémenté et testé avec des clients pour s'assurer que les mises à jour en temps réel sont correctement transmises.

### Tests effectués

- **Tests unitaire**s : Chaque processus a été testé individuellement pour s'assurer qu'il fonctionne correctement.
- **Tests d'intégration** : Les communications entre les processus ont été testées pour s'assurer qu'elles fonctionnent correctement.
- **Tests de performance** : La performance du système a été testée pour s'assurer qu'il peut gérer un grand nombre de véhicules.
- **Tests de robustesse** : Le système a été testé pour s'assurer qu'il peut gérer des scénarios de défaillance, tels que des processus qui se terminent de manière inattendue.

### Problèmes rencontrés et solutions

- **Problème** : Synchronisation des processus
  - **Solution** : Utilisation de sémaphores et d'événements  pour synchroniser les processus et s'assurer que les véhicules prioritaires passent en premier.
- **Problème** : Communication entre les processus
  - **Solution** : Utilisation de queues et de mémoire partagée pour la communication entre les processus, et de sockets pour la communication avec le serveur d'affichage.

### Exécution du programme

La simulation démarre avec le lancement du script principal `server.py`. Tout d’abord, les fonctions permettant de gérer le serveur (le démarrer, accepter des clients, gérer des clients, leur envoyer les informations, etc.) sont définies. On définit également une fonction qui permettra de fermer tous les processus que l’on utilisera plus tard.

Arrive ensuite la fonction `main`. Au début de celle-ci, on génère 4 signaux, représentant la présence (ou non) d’un véhicule prioritaire dans chaque direction du carrefour. On caractérise ensuite la mémoire partagée. Une liste qui correspond à l’état des feux, et une liste qui compte le nombre de véhicules dans chaque direction.

On définit ensuite 4 queues. Chacune stocke les véhicules dans une des 4 directions. On déclare également un manager. Ensuite, on crée un processus par fonction : génération de véhicules normaux et prioritaires, la gestion des feux ainsi que le coordinateur.

On entre ensuite dans une boucle `while` dont on peut sortir de 2 manières : soit la durée de la simulation arrive à son terme, soit il y a un bouchon dans une des directions. Dans cette boucle, le serveur envoie périodiquement toutes les informations nécessaires aux clients pour qu’ils puissent afficher l’état de la simulation dans une fenêtre Pygame. Quand la boucle finit, on ferme tous les processus grâce à la fonction définie précédemment.

Les clients quant à eux ont juste à lancer le script `client.py` et observer la simulation.

### Conclusion

De manière générale, ce projet a permis de mettre en pratique les concepts de programmation parallèle et concurrente pour simuler efficacement le trafic à une intersection. Grâce à l'utilisation de structures de données adaptées et de protocoles d'échange robustes, nous avons pu gérer le passage des véhicules normaux et prioritaires de manière ordonnée et sécurisée.

La simulation en temps réel, rendue possible par la communication entre le serveur et les clients via des sockets, offre une visualisation claire et précise de l'état de l'intersection. Le projet démontre l'importance de la coordination et de la synchronisation dans les systèmes parallèles et concurrents, et fournit une base solide pour des simulations de trafic plus complexes à l'avenir.

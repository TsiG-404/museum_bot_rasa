# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted
# Η κοινή mock βάση δεδομένων (κρατάμε τους τόνους εδώ για να φαίνονται ωραία στο print)
# Η κοινή mock βάση δεδομένων του μουσείου στην κορυφή του αρχείου
EXHIBITS_DB = {
    "παρθενώνα": "Ο Παρθενώνας είναι ναός δωρικού ρυθμού, αφιερωμένος στην Αθηνά.",
    "αφροδίτη της μήλου": "Το διάσημο άγαλμα της Αφροδίτης ανακαλύφθηκε το 1820. ",
    "δισκοβόλο": "Ο Δισκοβόλος του Μύρωνα είναι κλασικό έργο της αρχαίας ελληνικής γλυπτικής.",
    "ελ γκρέκο": "Ο Δομήνικος Θεοτοκόπουλος (Ελ Γκρέκο) ήταν κορυφαίος ζωγράφος της Ισπανικής Αναγέννησης.",
    "μηχανισμό των αντικυθήρων": "Ο Μηχανισμός των Αντικυθήρων θεωρείται ο πρώτος αναλογικός υπολογιστής της αρχαιότητας, σχεδιασμένος για τον υπολογισμό αστρονομικών θέσεων.",
    "ηνίοχο των δελφών": "Ο Ηνίοχος των Δελφών είναι ένα από τα σπουδαιότερα χάλκινα αγάλματα της πρώιμης κλασικής περιόδου που σώζονται μέχρι σήμερα.",
    "νίκη της σαμοθράκης": "Το εντυπωσιακό μαρμάρινο άγαλμα της Νίκης παριστάνει τη φτερωτή θεά να προσγειώνεται στην πλώρη ενός πλοίου.",
    "ερμή του πραξιτέλη": "Ένα από τα πιο γνωστά αριστουργήματα της αρχαίας γλυπτικής, που απεικονίζει τον θεό Ερμή να κρατάει τρυφερά τον μικρό θεό Διόνυσο.",
    "προσωπείο του αγαμέμνονα": "Το χρυσό νεκρικό προσωπείο ανακαλύφθηκε στις Μυκήνες. Αν και ονομάστηκε έτσι από τον Ερρίκο Σλήμαν, πιθανότατα ανήκει σε ηγεμόνα παλαιότερης εποχής.",
    "δίσκο της φαιστού": "Ο διάσημος πήλινος δίσκος της μινωικής εποχής περιέχει σύμβολα τυπωμένα σε σπειροειδή διάταξη, τα οποία παραμένουν ένα άλυτο μυστήριο.",
    "κούρο της αναβύσσου": "Ο Κούρος είναι ένα εξαιρετικό δείγμα αρχαϊκής γλυπτικής, με το χαρακτηριστικό 'αρχαϊκό μειδίαμα' (χαμόγελο) στο πρόσωπό του.",
    "ζωφόρο του παρθενώνα": "Μια εκπληκτική ανάγλυφη ζώνη που περιέτρεχε τον ναό, απεικονίζοντας την πομπή των Παναθηναίων, τη μεγαλύτερη γιορτή της αρχαίας Αθήνας.",
    "ρυτό των ταύρων": "Ένα μοναδικό τελετουργικό σκεύος από τη μινωική Κρήτη, φτιαγμένο από μαύρο στεατίτη σε σχήμα κεφαλιού ταύρου, με κέρατα από χρυσό.",
    "τοιχογραφία της άνοιξης": "Η πανέμορφη αυτή τοιχογραφία από το Ακρωτήρι της Σαντορίνης απεικονίζει ένα βραχώδες τοπίο με ανθισμένους κρίνους και χελιδόνια που πετούν."
}

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# 1. Βοηθητική συνάρτηση που αφαιρεί τόνους και τα κάνει όλα πεζά
def remove_accents(text):
    accents_map = {
        'ά': 'α', 'έ': 'ε', 'ή': 'η', 'ί': 'ι', 'ό': 'ο', 'ύ': 'υ', 'ώ': 'ω',
        'ϊ': 'ι', 'ϋ': 'υ', 'ΐ': 'ι', 'ΰ': 'υ'
    }
    text = text.lower()
    for accented, unaccented in accents_map.items():
        text = text.replace(accented, unaccented)
    return text




class ActionProvideExhibitInfo(Action):
    def name(self) -> Text:
        return "action_provide_exhibit_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        exhibit = tracker.get_slot("exhibit_name")

        if exhibit:
            # 2. Καθαρίζουμε αυτό που έγραψε ο χρήστης
            user_exhibit_clean = remove_accents(exhibit)
            
            info = None
            # 3. Ψάχνουμε στη βάση αγνοώντας τους τόνους
            for key, value in EXHIBITS_DB.items():
                if remove_accents(key) == user_exhibit_clean:
                    info = value
                    break
            
            if info:
                dispatcher.utter_message(text=info)
            else:
                dispatcher.utter_message(text=f"Δυστυχώς, δεν έχω ακόμα πληροφορίες για το έκθεμα '{exhibit}'.")
        else:
            dispatcher.utter_message(text="Δεν κατάλαβα ποιο έκθεμα ψάχνεις.")
        
        return []

#για να εμφανιζει την λιστα με διαθεσιμα εκθεματα
class ActionListAvailableExhibits(Action):
    def name(self) -> Text:
        return "action_list_available_exhibits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Παίρνουμε δυναμικά όλα τα κλειδιά από το EXHIBITS_DB και τα μορφοποιούμε με κεφαλαίο
        names = [exhibit.capitalize() for exhibit in EXHIBITS_DB.keys()]
        
        # Τα ενώνουμε σε ένα string χωρισμένα με κόμμα (π.χ. "Παρθενώνα, Δισκοβόλο...")
        exhibits_string = ", ".join(names)
        
        reply = f"Έχω διαθέσιμες πληροφορίες για τα εξής εκθέματα: {exhibits_string}. Για ποιο από αυτά συγκεκριμένα θα ήθελες να μάθεις;"
        dispatcher.utter_message(text=reply)
        
        return []
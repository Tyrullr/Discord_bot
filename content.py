from structures import TreeNode

def build_tree():
    res_g_1 = TreeNode("Gryffondor (L'Intrépide) ! Tu fonces sans réfléchir.", is_result=True)
    res_g_2 = TreeNode("Gryffondor (Le Noble) ! Tu défends les faibles.", is_result=True)
    
    res_s_1 = TreeNode("Serpentard (Le Rusé) ! La fin justifie les moyens.", is_result=True)
    res_s_2 = TreeNode("Serpentard (L'Ambitieux) ! Le pouvoir avant tout.", is_result=True)
    
    res_r_1 = TreeNode("Serdaigle (L'Erudit) ! La connaissance est ton arme.", is_result=True)
    res_r_2 = TreeNode("Serdaigle (Le Créatif) ! L'originalité te guide.", is_result=True)
    
    res_h_1 = TreeNode("Poufsouffle (Le Loyal) ! On peut compter sur toi.", is_result=True)
    res_h_2 = TreeNode("Poufsouffle (Le Travailleur) ! L'effort paie toujours.", is_result=True)

    q_duel = TreeNode("En duel, tu attaques (1) ou tu pièges (2) ?", left=res_g_1, right=res_s_1)
    q_leader = TreeNode("Tu veux être aimé (1) ou craint (2) ?", left=res_g_2, right=res_s_2)
    q_study = TreeNode("Tu préfères les Maths (1) ou l'Art (2) ?", left=res_r_1, right=res_r_2)
    q_friend = TreeNode("Un ami a tort. Tu le soutiens (1) ou tu le corriges (2) ?", left=res_h_1, right=res_h_2)

    q_action = TreeNode("Face au danger : Action immédiate (1) ou Planification (2) ?", left=q_duel, right=q_leader)
    q_calm = TreeNode("Dans le calme : Tu étudies (1) ou tu aides les autres (2) ?", left=q_study, right=q_friend)

    root = TreeNode("Au fond de toi, cherches-tu la Gloire (1) ou la Paix (2) ?", left=q_action, right=q_calm)
    
    return root

quiz_tree = build_tree()

encyclopedia = {
    "lumos": "Sortilège qui allume le bout de la baguette.",
    "nox": "Sortilège qui éteint la baguette.",
    "hippogriffe": "Créature mi-aigle, mi-cheval. Très susceptible.",
    "sombral": "Cheval squelettique visible seulement par ceux qui ont vu la mort.",
    "alohomora": "Déverrouille les portes.",
    "expelliarmus": "Sortilège de désarmement.",
    "patronus": "Bouclier de lumière positive contre les détraqueurs.",
    "imperium": "Sortilège impardonnable de contrôle mental.",
    "basilic": "Serpent géant dont le regard tue instantanément.",
    "mandragore": "Plante dont le cri peut tuer ceux qui l'entendent."
}

def tree_contains(node, topic):
    if not node:
        return False
    if topic.lower() in node.text.lower():
        return True
    return tree_contains(node.left, topic) or tree_contains(node.right, topic)
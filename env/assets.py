aluminumCan = [f'aluminumCan/can{i}.png' for i in range(10)]
aluminumCan_visibility = [2, 3, 3, 2, 3, 3, 3, 2, 3, 3]
cardboard = [f'cardboard/cardboard{i}.png' for i in range(10)]
cardboard_visibility = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
carton = [f'carton/carton{i}.png' for i in range(10)]
carton_visibility = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
glassBottle = [f'glassBottle/glassBottle{i}.png' for i in range(9)]
glassBottle_visibility = [3, 3, 2, 3, 3, 3, 2, 2, 3]
paper = [f'paper/paper{i}.png' for i in range(21)]
paper_visibility = [3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
paperBag = [f'paperBag/paperBag{i}.png' for i in range(15)]
paperBag_visibility = [3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3]
plasticBag = [f'plasticBag/plasticBag{i}.png' for i in range(23)]
plasticBag_visibility = [3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3]
# plasticBottle = [f'plasticBottle/plasticBottle{i}.png' for i in range(12)]
reject = [f'reject/reject{i}.png' for i in range(20)]
reject_visibility = [1, 2, 3, 3, 3, 1, 2, 3, 3, 1, 2, 1, 3, 1, 2, 3, 2, 2, 1, 2]

trash_classes = aluminumCan + cardboard + carton + glassBottle + paper + paperBag + plasticBag + reject
trash_visibility = aluminumCan_visibility + cardboard_visibility + carton_visibility + glassBottle_visibility + paper_visibility + paperBag_visibility + plasticBag_visibility + reject_visibility

trash_visibility = {trash_classes[i]: trash_visibility[i] for i in range(len(trash_classes))}
visibility_probability = {1: 0.85, 2: 0.9, 3: 0.98}
speed_probability = {0: 0.04, 1: 0.08, 2: 0.10}
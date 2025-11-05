from systems.processes import Fermentation, Filtration, Distillation, Dehydration

"""
# Test Fermentation class
test_fermenter = Fermentation(0.85)
print(test_fermenter.name)
print(test_fermenter.ferment({
    "ethanol": 0,
    "water": 100,
    "sugar": 50,
    "fiber": 20
}))

# Test Filtration class
test_filter = Filtration(0.90)
print(test_filter.name)
print(test_filter.filter({
    "ethanol": 25.5,
    "water": 100,
    "sugar": 7.5,
    "fiber": 20
}))

# Test Distillation class
test_distiller = Distillation(0.80)
print(test_distiller.name)
print(test_distiller.distill({
    "ethanol": 25.5,
    "water": 100,
    "sugar": 7.5,
    "fiber": 20
}))

# Test Dehydration class
test_dehydrator = Dehydration(0.95)
print(test_dehydrator.name)
print(test_dehydrator.dehydrate({
    "ethanol": 20.4,
    "water": 100,
    "sugar": 7.5,
    "fiber": 20
}))
"""

# Fermentation iteration test
test_fermenter = Fermentation(0.85)
input_stream = {
    "ethanol": [0, 0, 0],
    "water": [100, 100, 100],
    "sugar": [50, 40, 30],
    "fiber": [20, 20, 20]
}
print(test_fermenter.iterateInputs(input_stream))
print(test_fermenter.inputs)
print(test_fermenter.outputs)
test_fermenter.display("sugar", "ethanol")
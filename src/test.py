from model import Model

model = Model.load()

with model.prediction():
    model.use_unit_count(0, "Marine", 10)
    model.use_unit_count(0, "Reaper", 0)
    model.use_unit_count(1, "Marine", 10)
    model.use_unit_count(1, "Reaper", 0)
    q = model.make_prediction()


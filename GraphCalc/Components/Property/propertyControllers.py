from GraphCalc.Components.Property.property import Property, ToggleProperty, IntProperty


# A class that allows for any Object to bind a Property to it, which can be manipulated due to that
class PropertyController:
    def __init__(self, assignProperty=None):
        self.bindTo(assignProperty)

    def bindTo(self, targetProperty):
        self.assignedProperty = targetProperty


class TogglePropertyController(PropertyController):
    def __init__(self, assignProperty=None):
        assert isinstance(assignProperty, ToggleProperty)
        super().__init__(assignProperty)


class SliderPropertyController(PropertyController):
    def __init__(self, assignProperty=None):
        assert isinstance(assignProperty, IntProperty)
        super().__init__(assignProperty)


class InputPropertyController(PropertyController):
    def __init__(self, assignProperty=None):
        assert isinstance(assignProperty, Property)
        super().__init__(assignProperty)

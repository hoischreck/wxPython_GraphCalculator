from MyWx.wx import *

from GraphCalc.Components.Property.property import NumProperty, ListProperty, GraphicalPanelObject, ToggleProperty, \
    PropertyObjCategory
from GraphCalc._core.utilities import multiplesInInterval


class CartesianAxies(GraphicalPanelObject):
    def __init__(self):
        super().__init__(category=PropertyObjCategory.NO_CATEGORY)

        self.getProperty("name").setValue("Cartesian Coordinate-System")

    def setBasePlane(self, plane):
        # Properties must be set here, since update function requires panel
        # todo: is there a design that makes implementing the super method redundant?
        super().setBasePlane(plane)
        self.getProperty("selectable").setValue(False)
        self.addProperty(ToggleProperty("draw_sub_axis", True, updateFunction=self.refreshBasePlane))
        self.addProperty(ToggleProperty("draw_main_axis", True, updateFunction=self.refreshBasePlane))
        c = self.getProperty("color")
        c.setValue((0, 0, 0))
        c.setUpdateFunction(self.refreshBasePlane)
        self.addProperty(c, override=True)
        self.addProperty(
            ListProperty(
                "color_sub_axis",
                (122, 122, 122),
                fixedFieldAmount=3,
                validityFunction=lambda x: 0 <= x <= 255,
                updateFunction=self.refreshBasePlane
            )
        )
        self.addProperty(NumProperty("sub_axis_draw_width", 1, self.refreshBasePlane))

    # todo: add update function as paramter, so values are not newly calculated if id draw is happenening

    # blitUpdate must be implemented correctly (currently with old deviceContext logic for prototyping)
    # -> new version utilises blit from basePlane
    @GraphicalPanelObject.standardProperties
    def blitUpdate(self, deviceContext, **kwargs):  # TODO: update base class
        if self.getProperty("draw_sub_axis").getValue() is True:
            self.drawSubAxis(deviceContext, 50)
        if self.getProperty("draw_main_axis").getValue() is True:
            self.drawMainAxis(deviceContext)

    @GraphicalPanelObject.draw("color_sub_axis", "sub_axis_draw_width")
    def drawSubAxis(self, deviceContext, axisPixelDistance):
        xSubAxis = multiplesInInterval(axisPixelDistance, self._basePlane.db)
        ySubAxis = multiplesInInterval(axisPixelDistance, self._basePlane.wb)
        for x in xSubAxis:
            x, _ = self._basePlane.correctPosition(x, 0)
            deviceContext.DrawLine(x, 0, x, self._basePlane.h)
        for y in ySubAxis:
            _, y = self._basePlane.correctPosition(0, y)
            deviceContext.DrawLine(0, y, self._basePlane.w, y)

    @GraphicalPanelObject.draw("color", "draw_width")
    def drawMainAxis(self, deviceContext):
        # deviceContext = self.basePlane.memoryDc
        if self._basePlane.db[0] < 0 < self._basePlane.db[1]:
            x0, _ = self._basePlane.correctPosition(0, 0)  # combine functions
            deviceContext.DrawLine(x0, 0, x0, self._basePlane.h)
        if self._basePlane.wb[0] < 0 < self._basePlane.wb[1]:
            _, y0 = self._basePlane.correctPosition(0, 0)  # combine functions
            deviceContext.DrawLine(0, y0, self._basePlane.w, y0)

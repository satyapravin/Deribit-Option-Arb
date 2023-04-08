from PyQt6 import QtCore, QtGui

class PositionModel(QtCore.QAbstractTableModel): 
    def __init__(self, parent=None, *args): 
        super(PositionModel, self).__init__()
        self.positionData = None

        
    def update(self, positionData):
        self.positionData = positionData
     
    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.positionData.getRows()

        
    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.positionData.getCols()

        
    def data(self, index, role=QtCore.Qt):
        if self.positionData is not None:
            i = index.row()
            j = index.column()

            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                if j == 0 or i == 0:
                    return '{0}'.format(self.positionData.getData(i, j))
                elif i > 0 and j > 0:
                    return '{:.4f}'.format(self.positionData.getData(i, j))
            elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
                if j > 0 and i > 0:
                    return QtCore.Qt.AlignmentFlag.AlignRight
            elif role == QtCore.Qt.ItemDataRole.ForegroundRole:
                if j > 0 and i > 0:
                    if self.positionData.getData(i, j) > 0:
                        return QtGui.QBrush(QtCore.Qt.GlobalColor.darkBlue)
                    elif self.positionData.getData(i, j) < 0:
                        return QtGui.QBrush(QtCore.Qt.GlobalColor.darkRed)
            return QtCore.QVariant()
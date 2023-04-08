from PyQt6 import QtCore, QtGui

class SelectionModel(QtCore.QAbstractTableModel): 
    def __init__(self, parent=None, *args): 
        super(SelectionModel, self).__init__()
        self.selectionData = None

        
    def update(self, selectionData):
        self.selectionData = selectionData
     
    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.selectionData.getRows()

        
    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.selectionData.getCols()

        
    def data(self, index, role=QtCore.Qt):
        if self.selectionData is not None:
            i = index.row()
            j = index.column()

            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                if j == 0 or i == 0:
                    return '{0}'.format(self.selectionData.getData(i, j))
                elif i > 0 and j > 0:
                    return '{:.4f}'.format(self.selectionData.getData(i, j))
            elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
                if j > 0 and i > 0:
                    return QtCore.Qt.AlignmentFlag.AlignRight
            elif role == QtCore.Qt.ItemDataRole.ForegroundRole:
                if j > 0 and i > 0:
                    if self.selectionData.getData(i, j) > 0:
                        return QtGui.QBrush(QtCore.Qt.GlobalColor.darkBlue)
                    elif self.selectionData.getData(i, j) < 0:
                        return QtGui.QBrush(QtCore.Qt.GlobalColor.darkRed)
            return QtCore.QVariant()
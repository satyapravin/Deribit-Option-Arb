from PyQt6 import QtCore, QtGui

class ResultsModel(QtCore.QAbstractTableModel): 
    def __init__(self, parent=None, *args): 
        super(ResultsModel, self).__init__()
        self.results = None

        
    def update(self, results):
        self.results = results
     
    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.results.getRows()

        
    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.results.getCols()

        
    def data(self, index, role=QtCore.Qt):
        if self.results is not None:
            i = index.row()
            j = index.column()

            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                if i == 0:
                    return '{0}'.format(self.results.getData(i, j))
                else:
                    return '{:.4f}'.format(self.results.getData(i, j))
            elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
                if i > 0:
                    return QtCore.Qt.AlignmentFlag.AlignRight
            elif role == QtCore.Qt.ItemDataRole.ForegroundRole:
                if i > 0:
                    if self.results.getData(i, j) > 0:
                        return QtGui.QBrush(QtCore.Qt.GlobalColor.darkBlue)
                    elif self.results.getData(i, j) < 0:
                        return QtGui.QBrush(QtCore.Qt.GlobalColor.darkRed)
            return QtCore.QVariant()
from PyQt6 import QtCore, QtGui
from account_data import AccountData

class AccountModel(QtCore.QAbstractTableModel): 
    def __init__(self, parent=None, *args): 
        super(AccountModel, self).__init__()
        self.accountData = None

        
    def update(self, accountData):
        self.accountData = accountData

     
    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.accountData.getRows()

        
    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.accountData.getCols()

        
    def data(self, index, role=QtCore.Qt):
        if self.accountData is not None:
            i = index.row()
            j = index.column()

            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                if j == 0 or i == 0:
                    return '{0}'.format(self.accountData.getData(i, j))
                elif i > 0 and j == 1:
                    return '{:.8f}'.format(self.accountData.getData(i, j))
            elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
                if j == 1:
                    return QtCore.Qt.AlignmentFlag.AlignRight
            elif role == QtCore.Qt.ItemDataRole.ForegroundRole:
                if j == 1 and i > 0:
                    if self.accountData.getData(i, j) > 0:
                        return QtGui.QBrush(QtCore.Qt.GlobalColor.darkBlue)
                    elif self.accountData.getData(i, j) < 0:
                        return QtGui.QBrush(QtCore.Qt.GlobalColor.darkRed)
            return QtCore.QVariant()
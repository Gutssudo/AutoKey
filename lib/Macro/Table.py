#QtTable https://www.developpez.net/forums/d2145636/autres-langages/python/gui/pyqt/combobox-qtablewidget/
import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox, QLineEdit
from PyQt5.QtGui import QDoubleValidator

class TableWidget(QTableWidget):
	def __init__(self, actions):
		super().__init__()
		self.actions=actions
		# self.table = QTableWidget(self)
		# self.setRowCount(len(self.actions))  # Nombre de lignes
		self.setColumnCount(2)  # Nombre de colonnes

		self.setHorizontalHeaderLabels(['Actions', 'Settings'])

		
		self.add_list_to_row(0,self.actions)


		#combo


		# layout = QVBoxLayout()
		# layout.addWidget(self.table)
		# self.setLayout(layout)
    
	def add_list_to_row(self, column, items):
		if self.actions is not None:
			for row, item in enumerate(items):
				self.insertRow(self.rowCount())
				table_item = QTableWidgetItem(item)
				self.setItem(self.rowCount() - 1, 0, table_item)  # Remplit la colonne 0 de la nouvelle ligne
			self.Colum1Row()
	
	def delayCell(self,row, column ):
		self.delayInput = QLineEdit()
		self.delayInput.setPlaceholderText("time (s)")
		self.delayInput.setValidator(QDoubleValidator(0.99, 99.99, 2))
		self.setCellWidget(row, column, self.delayInput)


	def comboCell(self, row, column):
		combo = QComboBox()
		combo.addItems(["presser", "maintenir", "relâcher"]) 
		self.setCellWidget(row, column, combo)

	def Colum1Row(self):
		for row in range(self.rowCount()):
			if self.item(row, 0) != None:
				if self.item(row, 0).text() == 'delay':
					self.delayCell(row, 1)
				else:
					self.comboCell(row, 1)

	def addDelayItem(self):
		self.insertRow(self.rowCount())
		delay_item = QTableWidgetItem('delay')
		self.setItem(self.rowCount() - 1, 0, delay_item)  
		self.Colum1Row()

	def RemoveAllRow(self):
		for row in reversed(range(0,self.rowCount()+1)):
			self.removeRow(row)

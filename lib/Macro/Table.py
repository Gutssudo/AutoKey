#QtTable https://www.developpez.net/forums/d2145636/autres-langages/python/gui/pyqt/combobox-qtablewidget/
import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox, QLineEdit
from PyQt5.QtGui import QDoubleValidator
import re 
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
				self.Colum1Row(self.rowCount()-1)

	def loadFileTable(self, column, items):
		if self.actions is not None:
	# Remplir le QTableWidget avec les données
			# print(type(items))
			# for item in items :
			# 	print(item) 
			for row, (col1, col2) in enumerate(items):
				patternDelay = r'^\d+$'
				matchDelay = bool(re.match(patternDelay,col1))
				if matchDelay != True : 
					self.insertRow(self.rowCount())
					col1 = QTableWidgetItem(col1)
					self.setItem(row, 0, col1)
					self.comboCell(row, 1, col2)

				else :
					self.addDelayItem(row)
					print(col2)
					self.delayCell(row, 1, col1)
			# self.setItem(row, 1, QTableWidgetItem(col2))  # Remplir la deuxième colonne
			# print(col1, col2)
			# table.setItem(row_index, 1, QTableWidgetItem(col2))

			self.viewport().update()

	
	def delayCell(self,row, column, value=None ):
		self.delayInput = QLineEdit()
		self.delayInput.setPlaceholderText("time (s)")
		self.delayInput.setValidator(QDoubleValidator(0.99, 99.99, 2))
		self.setCellWidget(row, column, self.delayInput)
		self.delayInput.setText(value)

	def comboCell(self, row, column, value=None):
		self.combo = QComboBox()
		self.combo.addItems(["presser", "maintenir", "relâcher"]) 
		self.setCellWidget(row, column, self.combo)
		if value is not None or value is not False:
			if value.lower() == 'up':
				index = self.combo.findText('relâcher')
				self.combo.setCurrentIndex(index) 
			elif value.lower() == 'down' : 
				index = self.combo.findText('presser')
				self.combo.setCurrentIndex(index) 

	def Colum1Row(self, row):
		# for row in range(self.rowCount()):
		if self.item(row, 0) != None:
			if self.item(row, 0).text() == 'delay':
				self.delayCell(row, 1)
			else:
				self.comboCell(row, 1)
		# else:
		# 	pass


	def addDelayItem(self, row=None):
		if row is None or row is False:
			row = self.rowCount()
			print(row)
		self.insertRow(row)
		delay_item = QTableWidgetItem('delay')
		self.setItem(row , 0, delay_item)  
		self.Colum1Row(row)

	def RemoveAllRow(self):
		for row in reversed(range(0,self.rowCount()+1)):
			self.removeRow(row)

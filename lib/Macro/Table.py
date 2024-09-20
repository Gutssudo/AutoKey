#QtTable https://www.developpez.net/forums/d2145636/autres-langages/python/gui/pyqt/combobox-qtablewidget/
import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox, QLineEdit
from PyQt5.QtGui import QDoubleValidator
import re 
class TableWidget(QTableWidget):
	def __init__(self):
		super().__init__()
		self.actions=None
		# self.table = QTableWidget(self)
		# self.setRowCount(len(self.actions))  # Nombre de lignes
		self.setColumnCount(2)  # Nombre de colonnes

		self.setHorizontalHeaderLabels(['Actions', 'Settings'])

		
		# self.add_list_to_row(0,self.actions)


		#combo


		# layout = QVBoxLayout()
		# layout.addWidget(self.table)
		# self.setLayout(layout)
	
	def addActions(self, column, action):
		self.insertRow(self.rowCount())
		table_item = QTableWidgetItem(action)
		self.setItem(self.rowCount() - 1, 0, table_item)  # Remplit la colonne 0 de la nouvelle ligne

	def loadFileTable(self, items, yaml):
		if items is not None:
	# Remplir le QTableWidget avec les données

			for col1, col2 in items:
				patternDelay = r'^\d+$'
				matchDelay = bool(re.match(patternDelay,col1))
				row = self.rowCount()
				# print(row, col1, col2)
				if matchDelay is True and yaml is not True:
					self.addDelayItem(row)
					self.delayCell(row, 1, col1)
				

				elif matchDelay is False : 
					col1item = QTableWidgetItem(col1)
					if col1 == 'delay':
						self.addDelayItem(row)
						self.delayCell(row, 1, col2)
					else: 
						# self.insertRow(self.rowCount())
						# self.setItem(row, 0, col1)
						self.addActions(0,col1item)
						self.comboCell(row, 1, col2)



			# else : 
			# 	for row, (col1, col2) in enumerate(items):
			# 		if col1 == 'delay' : 


			# self.setItem(row, 1, QTableWidgetItem(col2))  # Remplir la deuxième colonne
			# print(col1, col2)
			# table.setItem(row_index, 1, QTableWidgetItem(col2))

			self.viewport().update()

	
	def delayCell(self,row, column, value=None ):
		self.delayInput = QLineEdit()
		self.delayInput.setPlaceholderText("time (s)")
		self.delayInput.setValidator(QDoubleValidator(0.99, 99.99, 2))
		self.setCellWidget(row, column, self.delayInput)
		if value is not None : 
			self.delayInput.setText(str(value))

	def comboCell(self, row, column, value=None):
		self.combo = QComboBox()
		self.combo.addItems(["presser", "relâcher"]) 
		self.setCellWidget(row, column, self.combo)
		if value is not None and value is not False:
			if str(value).lower() == 'up' or str(value) =="relâcher":
				index = self.combo.findText('relâcher')
				self.combo.setCurrentIndex(index) 
			elif str(value).lower() == 'down' or str(value) =="presser" : 
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
			# print(row)
		self.insertRow(row)
		delay_item = QTableWidgetItem('delay')
		self.setItem(row , 0, delay_item)  
		self.Colum1Row(row)

	def RemoveAllRow(self):
		for row in reversed(range(0,self.rowCount()+1)):
			self.removeRow(row)

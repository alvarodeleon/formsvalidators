import re


class Validators:

	def rules(self,value,rules):

		check = True

		explode_rules = rules.split(',')

		if value is not None:

			for rule in explode_rules:

				if rule=='!empty':
					if self.empty(value):
						check = False

				if rule=='!none':
					if value is None:
						check = False
				
				if rule=='domain':
					if not self.domain(value):
						check = False

				if rule=='ip':
					if not self.ip(value):
						check = False

				if rule=='mail':
					if not self.mail(value):
						check = False

				if rule=='integer':
					if not self.integer(value):
						check = False

				if rule=='float':
					if not self.float(value):
						check = False

				if rule=='numeric':
					if not self.numeric(value):
						check = False

				if rule=='filename':
					if not self.numeric(value):
						check = False

			return check
		else:
			return False



	#Arrays
	def options(self,value,options):
		if value in options:
			return True
		else:
			return False

	#Contents

	def domain(self,value):
		return re.match("^(?=.{1,255}$)(?!-)[A-Za-z0-9\-]{1,63}(\.[A-Za-z0-9\-]{1,63})*\.?(?<!-)$",value)

	def ip(self,value):
		return re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",value)

	def mail(self,value):

		#if re.match('^[a-z0-9\.]+[@]\w+[.]\w{2,3}+[.]\w{2,3}$',value) or re.match('^[a-z0-9\.]+[@]\w+[.]\w{2,3}$',value):
		#if re.match("^[a-z0-9\.]+[@][a-z0-9\.].+[.]\w{2,3}$",value):
		if re.match("^[a-z0-9\.]+[@][a-z0-9\.].+[.]\w.*$",value):

			return True 
		else:
			return False

	def filename(self,value):
		return re.match("^[A-Za-z0-9\_\-\.]+$",value)

	#States

	def empty(self,value):

		if self.numeric(value):
			if value < 1:
				return True
			else:
				return False
		
			if len(value)<1:
				return True
			else:
				return False
		elif self.string(value):
			if len(value)<1:
				return True
			else:
				return False


	#types
	def string(self,value):
		try:
			val = str(value)
			return True
		except:
			return False

	def integer(self,value):
		try:
			val = int(value)
			return True
		except:
			return False

	def float(self,value):
		try:
			val = float(value)
			return True
		except:
			return False

	def numeric(self,value):
		if self.integer(value) or self.float(value):
			return True
		else:
			return False


class FormValidation:

	__data = None
	__errors = []
	__fields_cheched = []

	def __init__(self,data):
		self.__data = data	

	def rules(self,field,rules,options=None):
		
		#Validation with validators
		validator = Validators()
		
		
		if field in self.__data:
			
			if not validator.rules(self.__data[field],rules):
				self.__errors.append('{} is not valid'.format(field))

					
			self.__fields_cheched.append(field)

		#Required
		explode_rules = rules.split(',')

		for rule in explode_rules:

			if rule=='required':
				if field not in self.__data:
					self.__errors.append('{} is required'.format(field))

			if rule=='options':
				if field in self.__data:
					if not validator.options(self.__data[field],options):
						self.__errors.append('{} is not valid'.format(field))			

				

	def getErrors(self):
		return self.__errors

	def getData(self):
		return self.__data

	def check(self):
		tmp = {}	

		for field in self.__data:
			if field in self.__fields_cheched:
				tmp[field] = self.__data[field]

		self.__data = tmp

		if len(self.__errors)>0:
			return False
		else:
			return True

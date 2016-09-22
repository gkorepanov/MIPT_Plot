#from numpy import *
import Gnuplot, Gnuplot.funcutils, os, pyperclip, sys, copy
#s_settings = ["output","x_title","y_title","term"]
#i_settings = ["x_min","x_max","y_min","y_max","font_size"]


epslatex_settings = '''
set format xy "$%g$"
set ylabel offset 2.3, 0

set rmargin 0.1
set lmargin 3.5

'''

# Common settings, running everything
class C_Plotter(object):
	def __init__(self):
		self.font_size = "22"
		self.term = "epslatex"
		self.term_x = '16.5cm'
		self.term_y = '12cm'
		self.output = "out.tex"

		self.x_title = None
		self.y_title = None

		
		self.x_min = None
		self.x_max = None
		self.y_min = None
		self.y_max = None

		self.extra = ""
		self.plots = []

		self.g = Gnuplot.Gnuplot(debug=0)

# Each plot specific settings
class C_Plot(object):
	index = 0
	def __init__ (self):
		C_Plot.index +=1
		self.tempname = "data" + str(C_Plot.index) + '.mptplt'
		self.fit = 0
		self.plots_num = 1

		self.x_error = 0
		self.y_error = 0

		self.label = 0
		self.label_x = None
		self.label_y = None
		self.text = None
		
		self.extra = ""

		self.color = None

		self.accuracy = 2



def parse(line):
	line = line.lstrip(' ').rstrip('\n')
	if not line or line[0] == '#':
		return 0

	items = line.split(' ', 1)
	if len(items) == 1:
		name = items[0]
		value = None
	else:
		[name, value] = items

	name = name.rstrip(':')

	#print line
	return [name, value]


def loadsettings(self, filename):
	file = open(filename, "r")
	
	for line in file:
		ret = parse(line)
		if ret:
			[name, value] = ret
				
			if name == "output":
				self.output = value

			elif name == "x_title":
				self.x_title = value
			elif name == "y_title":
				self.y_title = value

			elif name == "x_min":
				self.x_min = float(value)
			elif name == "x_max":
				self.x_max = float(value)
			elif name == "y_min":
				self.y_min = float(value)
			elif name == "y_max":
				self.y_max = float(value)

			elif name == "font_size":
				self.font_size = int(value)

			elif name == "term":
				self.term = value
			elif name == "term_x":
				self.term_x = value
			elif name == "term_y":
				self.term_y = value

			elif name == "extra":
				self.extra = self.extra + value + '\n'
			else: 
				pass


# TODO: revise
def loadfile(self, filename):
	file = open(filename, "r")


	plot = C_Plot()
	
	for line in file:
		ret = parse(line)
		if ret:
			[name, value] = ret
			if name == "x_error":
				plot.x_error = int(value)
			elif name == "y_error":
				plot.y_error = int(value)

			elif name == "label":
				plot.label = int(value)
			elif name == "label_x":
				plot.label_x = int(value)
			elif name == "label_y":
				plot.label_y = int(value)
			elif name == "text":
				plot.text = value

			elif name == "extra":
				plot.extra = plot.extra + value + '\n'

			elif name == "color":
				plot.color = int(value)

			elif name == "fit":
				plot.fit = int(value)
			elif name == "plots_num":
				plot.plots_num = int(value)

			elif name == "accuracy":
				plot.accuracy = int(value)


			elif name == "data":
				break
			else: 
				pass

	self.copydata(file, plot)
	file.close()

# TODO: revise and join with previous
def copydata(self, file, plot):
	tempfile = open(plot.tempname, "w")
	for line in file:
		if parse(line):
			tempfile.write(' '.join(line.strip(' \n').replace(',', '.').split(' ')))
			tempfile.write('\n')


	self.plots.append(plot)
	file.close()
	tempfile.close()

	


def init_g(self, preview):
	if preview:
		s = 'set term wxt size 1600,900 '
		s += 'font "sansserif, ' + self.font_size + '"\n'
		#s += 'set multiplot\n'

		self.g(s)

		s = '''
		set grid ytics lc rgb "#bbbbbb" lw 1 lt 0
		set grid xtics lc rgb "#bbbbbb" lw 1 lt 0

		set grid mytics lc rgb "#cccccc" lw 1 lt 0
		set grid mxtics lc rgb "#cccccc" lw 1 lt 0

		set fit errorvariables


		unset key
		'''

		self.g(s)
		self.g(self.extra)

		
		if self.x_title is not None:
			self.g.xlabel(self.x_title)

		if self.y_title is not None:
			self.g.ylabel(self.y_title)

		if (self.x_min is not None) and (self.x_max is not None):
			self.g('set xrange [' + str(self.x_min) + ':' + str(self.x_max) + ']')

		if (self.y_min is not None) and (self.y_max is not None):
			self.g('set yrange [' + str(self.y_min) + ':' + str(self.y_max) + ']')




	else:
		raw_input(' ')
		#self.g.reset()
		self.g('unset key')
		self.g('set output "' + self.output + '"')


		s = 'set term ' + self.term + ' size ' + self.term_x + ',' + self.term_y + ' '
		s += 'font "sansserif, ' + self.font_size + '"\n'
		s += 'set multiplot\n'

		self.g(s)

		if self.term == "epslatex":
			self.g(epslatex_settings)
		


def plot(self, preview = 0):
	self.init_g(preview)

	if (preview):
		self.s_plot = ""

		index = 0

		for plot in self.plots:
			column = 1

			for i in xrange(1, plot.plots_num+1):
				index += 1
				self.g('print "---------------------------------------------------------------------------------------------"')
				self.g('print "PLOTTING Graph number ' + str(index)+'"')
				self.g('print "---------------------------------------------------------------------------------------------"')

				if plot.color is None:
					color = i
				else:
					color = plot.color

				s = 'set style line ' + str(index*2) +' lc ' + str(color) + ' pt 7 ps 1.5 lt 5 lw 3\n'
				s += 'set style line ' + str(index*2-1) + ' lc ' + str(color) + ' pt 7 ps 0 lt 5 lw 1\n'
					

				s += plot.extra

				self.g(s)


				s_using_main = str(column) + ':' + str(column+1)

				if plot.fit:
					self.g('f'+str(index)+'(x)=a'+str(index)+'*x+b'+str(index)+'')
					self.g('fit f'+str(index)+'(x) "' + plot.tempname + '" using ' + s_using_main + ' via a'+str(index)+',b'+str(index)+'')

				if plot.label and plot.fit and (plot.plots_num == 1):
					s = 'set label sprintf('+\
					('"$K = \\\\left(%.' + str(plot.accuracy) + 'f\\\\pm%.' + str(plot.accuracy) + 'f\\\\right)$ ' if self.term == "epslatex" else '"K = (%.' + str(plot.accuracy) + 'f+-%.' + str(plot.accuracy) + 'f) ')+\
					(plot.text if plot.text else "")+\
					'", a'+str(index)+', a'+str(index)+'_err)'



					if (plot.label_x is not None) and (plot.label_y is not None):
						s += ' at '+str(plot.label_x)+','+\
						str(plot.label_y)
					elif (self.x_max is not None) and (self.y_max is not None):
						s += ' at '+str(self.x_max*0.1)+','+\
						str(self.y_max*0.9)


					self.g(s)
			
		

				filename =  '"' + plot.tempname + '"'


				if plot.x_error and plot.y_error:
					s_using = ':'.join(map(str, xrange(column, column+4)))
					column += 3
					s_with = 'xyerrorbars'

				elif plot.x_error:
					s_using = ':'.join(map(str, xrange(column, column+3)))
					column += 2
					s_with = 'xerrorbars'

				elif plot.y_error:
					s_using = ':'.join(map(str, xrange(column, column+3)))
					column += 2
					s_with = 'yerrorbars'

				else:
					s_using = ':'.join(map(str, xrange(column, column+2)))
					column += 2
					s_with = 'points'

				s = filename + ' using ' + s_using_main +\
						' ls ' + str(index*2) +', '+ filename + ' using '+\
						s_using + ' ls ' + str(index*2-1) + ' with ' + s_with

					
				if plot.fit:
					s +=	', f'+str(index)+'(x) ls ' + str(index*2) +' with lines'

				#self.g(s)
				self.s_plot += s + ', '

		self.index = index

	self.g('plot ' + self.s_plot.rstrip(' ,'))
				
def dump(self):
	self.g('print "\\n\\n                 K               K_err"')
	for i in xrange(1, self.index+1):
		s = 'print "Graph N '+str(i)+' ", a'+str(i)+', a' +str(i)+'_err, "\\n"'
		self.g(s)



		

C_Plotter.copydata = copydata
C_Plotter.loadsettings = loadsettings
C_Plotter.loadfile = loadfile
C_Plotter.plot = plot
C_Plotter.init_g = init_g
C_Plotter.dump = dump


# TODO: everywhere, implement error checks
if __name__ == "__main__":

	if (len(sys.argv) < 2):
		print "Using: MIPT_Plot.py [settings] [datafile1] [datafile2]..."
		sys.exit()

	plotter = C_Plotter()
	
	plotter.loadsettings(sys.argv[1])

	for argv in (sys.argv[2:]):
		plotter.loadfile(argv)

	plotter.plot(preview=1)
	plotter.plot(preview=0)
	plotter.dump()
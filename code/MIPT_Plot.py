#from numpy import *
import Gnuplot, Gnuplot.funcutils, os, pyperclip, sys, copy
#s_settings = ["output","x_title","y_title","term"]
#i_settings = ["x_min","x_max","y_min","y_max","font_size"]


epslatex_settings = 'set format xy "$%g$"'

# Common settings, running everything
class C_Plotter(object):
	def __init__(self):
		self.font_size = "22"
		self.term = "epslatex"
		self.term_x = '16.5cm'
		self.term_y = '10cm'
		self.output = "out.tex"

		self.x_title = None
		self.y_title = None

		
		self.x_min = None
		self.x_max = None
		self.y_min = None
		self.y_max = None

		self.extra = ""
		self.plots = []

		self.g = Gnuplot.Gnuplot(debug=1)

# Each plot specific settings
class C_Plot(object):
	index = 0
	def __init__ (self):
		C_Plot.index +=1
		self.tempname = "data" + str(C_Plot.index) + '.dat'
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

	print line
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
		s += 'set multiplot\n'

		self.g(s)

	else:
		self.g.reset()
		self.g('unset multiplot')
		self.g('set output "' + self.output + '"')


		s = 'set term ' + self.term + ' size ' + self.term_x + ',' + self.term_y + ' '
		s += 'font "sansserif, ' + self.font_size + '"\n'
		s += 'set multiplot\n'

		self.g(s)

		if self.term == "epslatex":
			self.g(epslatex_settings)
		


def plot(self, preview = 0):
	self.init_g(preview)


	if self.x_title is not None:
		self.g.xlabel(self.x_title)

	if self.y_title is not None:
		self.g.ylabel(self.y_title)

	if (self.x_min is not None) and (self.x_max is not None):
		self.g('set xrange [' + str(self.x_min) + ':' + str(self.x_max) + ']')

	if (self.y_min is not None) and (self.y_max is not None):
		self.g('set yrange [' + str(self.y_min) + ':' + str(self.y_max) + ']')


	for plot in self.plots:
		column = 1

		for i in xrange(1, plot.plots_num+1):

			print "---------------------------------------------------------------------------------------------"
			print "PLOTTING Graph number " + str(i)
			print "---------------------------------------------------------------------------------------------"

			if plot.color is None:
				color = i
			else:
				color = plot.color

			s = '''
				set style line 1 lc ''' + str(color) + ''' pt 7 ps 1.2 lt 5 lw 3
				set style line 2 lc ''' + str(color) + ''' pt 7 ps 0 lt 5 lw 1

				set grid ytics lc rgb "#bbbbbb" lw 1 lt 0
				set grid xtics lc rgb "#bbbbbb" lw 1 lt 0
	
				set grid mytics lc rgb "#cccccc" lw 1 lt 0
				set grid mxtics lc rgb "#cccccc" lw 1 lt 0

				set fit errorvariables

				unset key
				'''

			s += plot.extra

			self.g(s)


			s_using_main = str(column) + ':' + str(column+1)

			if plot.fit:
				self.g('f(x)=a*x+b')
				self.g('fit f(x) "' + plot.tempname + '" using ' + s_using_main + ' via a,b')

			if plot.label and plot.fit and (plot.plots_num == 1):
				s = 'set label sprintf('+\
				('"$K = %.2f\\\\pm%.2f$' if self.term == "epslatex" else '"K = %.2f+-%.2f')+\
				(plot.text if plot.text else "")+\
				'", a, a_err)'



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

			s = 'plot ' + filename + ' using ' + s_using_main +\
					' ls 1, '+ filename + ' using '+\
					s_using + ' ls 2 with ' + s_with

				
			if plot.fit:
				s +=	', f(x) ls 1 with lines'

			self.g(s)
			if preview:
				raw_input('')


C_Plotter.copydata = copydata
C_Plotter.loadsettings = loadsettings
C_Plotter.loadfile = loadfile
C_Plotter.plot = plot
C_Plotter.init_g = init_g


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
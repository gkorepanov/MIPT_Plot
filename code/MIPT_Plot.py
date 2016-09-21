from numpy import *
import Gnuplot, Gnuplot.funcutils, os, pyperclip, sys



class C_Plot(object):
	def __init__ (self):
		self.filename = None
		self.tempname = None
		self.xerror = None
		self.yerror = None
		self.xtitle = None
		self.ytitle = None
		self.output = None
		self.ylimits = None
		self.xlimits = None

		self.label = None
		self.labelx = None
		self.labely = None
		self.labeltext = None
		self.fontsize = "22"
		self.term = "epslatex"

		self.xmax = 0
		self.ymax = 0

		self.fit = 1
		self.extra = ""





# TODO: revise
def load(self):
	file = open(self.filename, "r")

	for line in file:
		items = line.rstrip("\n").split(' ')
		items[0] = items[0][0:-1]
		#print items
		if items[0] == "x_error":
			self.xerror = int(items[1])
		elif items[0] == "y_error":
			self.yerror = int(items[1])
		elif items[0] == "output":
			self.output = items[1]

		elif items[0] == "x_title":
			self.xtitle = ' '.join(items[1:])
		elif items[0] == "y_title":
			self.ytitle = ' '.join(items[1:])
		elif items[0] == "x_limits":
			self.xlimits = '['+items[1]+':'+items[2]+']'
			self.xmax = int(items[2])
		elif items[0] == "y_limits":
			self.ylimits = '['+items[1]+':'+items[2]+']'
			self.ymax = int(items[2])

		elif items[0] == "label":
			self.label = items[1]
		elif items[0] == "label_x":
			self.labelx = items[1]
		elif items[0] == "label_y":
			self.labely = items[1]
		elif items[0] == "label_text":
			self.labeltext = ' '.join(items[1:]).strip('"')
		elif items[0] == "font_size":
			self.fontsize = items[1]
		elif items[0] == "term":
			self.term = ' '.join(items[1:])


		elif items[0] == "extra":
			self.extra = self.extra + ' '.join(items[1:])+'\n'

		elif items[0] == "fit":
			self.fit = int(items[1])

		elif items[0] == "data":
			break
		else: 
			pass

	self.copydata(file)
	file.close()

# TODO: revise and join with previous
def copydata(self, file):
	if not self.output:
		print "Wrong file format"
		sys.exit(1)

	tempfile = open(self.tempname, "w")
	for line in file:
		if line == '\n' or not line or line[0] == '#':
			pass
		else:
			tempfile.write(line.replace(",", "."))
	
	tempfile.close()
	file.close()


def setup_g(plot, g, preview):
	if preview:
		g('set term wxt size 1600,900 font "sansserif, '+\
		plot.fontsize+'"')
		g('set multiplot')

	else:
		g('unset multiplot')
		g('set output "'+plot.output+'"')

#TODO: just random values for A4 paper LaTeX. Give chance to change.
		if plot.term == "epslatex":
			g('set term epslatex size 16.5cm,10cm')
			g('set format xy "$%g$"')


		else:
			g('set term '+plot.term+' size 1600,900 font "sansserif, '+\
			plot.fontsize+'"')

		g('set multiplot')



def do(self, g, preview, color=7):
	if self.fit:
		g('f(x)=a*x+b')
# Using of temporary file. TODO.
		g('fit f(x) "'+\
			self.tempname+\
			'" using 1:2 via a,b')


	g('unset key')
# TODO: just random values. Make settings
	


	if self.xtitle:
		g.xlabel(self.xtitle)
	if self.ytitle:
		g.ylabel(self.ytitle)


#set style line 1 lc rgb \'black\' pt 7 ps 1.2 lt 5 lw 3
	#set style line 2 lc rgb \'black\' pt 7 ps 0 lt 5 lw 1

# TODO: give chance to change style


	g('''

	set style line 1 lc ''' + str(color) + ''' pt 7 ps 1.2 lt 5 lw 3
	set style line 2 lc ''' + str(color) + ''' pt 7 ps 0 lt 5 lw 1

	set grid ytics lc rgb "#bbbbbb" lw 1 lt 0
	set grid xtics lc rgb "#bbbbbb" lw 1 lt 0
	
	set grid mytics lc rgb "#cccccc" lw 1 lt 0
	set grid mxtics lc rgb "#cccccc" lw 1 lt 0

	set fit errorvariables

	
	''')

	g(self.extra)

	if self.xlimits:
		g('set xrange ' + self.xlimits)
	if self.ylimits:
		g('set yrange ' + self.ylimits)



	if self.label and self.fit:
		s = 'set label sprintf('+\
		('"$K = %.2f\\\\pm%.2f$' if self.term == "epslatex" else '"K = %.2f+-%.2f')+\
		(self.labeltext if self.labeltext else "")+\
		'",a, a_err)'



		if self.labelx and self.labely:
			s = s+' at '+str(self.labelx)+','+\
			str(self.labely)
		else:
			s = s+' at '+str(self.xmax*0.1)+','+\
			str(self.ymax*0.9)


		g(s)

	s1 =  ' "' + self.tempname +'"'
	s = 'plot ' + s1+' using 1:2 ls 1,' + s1


	if self.xerror and self.yerror:
		s = s+' using 1:2:4:3 ls 2 with xyerrorbars'
	elif self.xerror:
		s = s+' using 1:2:3 ls 2 with xerrorbars'
	elif self.yerror:
		s = s+' using 1:2:3 ls 2 with yerrorbars'
	else:
		s = s+' using 1:2 ls 2 with points'
		
	if self.fit:
		s = s +	', f(x) ls 1 with lines'

	g(s)


C_Plot.do = do
C_Plot.copydata = copydata
C_Plot.load = load


# TODO: everywhere, implement error checks
if __name__ == "__main__":

	plots = []
	i = 0

	for argv in (sys.argv[1:]):
		print argv
		plot = C_Plot()
		plot.filename = argv
		plot.tempname = "temp"+str(i)+".dat"
		plot.load()
		plots.append(plot)
		i=i+1

	g = Gnuplot.Gnuplot(debug=1)
	setup_g(plots[0], g, preview = 1)

	j = 1
	for plot in plots:
		if i == 1:
			plot.do(g, preview = 1)
		else: 
			plot.do(g, preview = 1, color=j)
		j = j+1

	raw_input(' ')

	setup_g(plots[0], g, preview = 0)

	i = j
	for plot in plots:
		plot.do(g, preview = 0, color=j)
		j=j+1

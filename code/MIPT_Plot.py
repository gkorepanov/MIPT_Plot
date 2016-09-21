from numpy import *
import Gnuplot, Gnuplot.funcutils, os, pyperclip, sys


class C_Data(object):
	pass

class C_Plot(object):
	def __init__ (self):
		self.filename = None
		self.xscale = 1.3
		self.yscale = 1.1
		self.tempname = "temp.dat"
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
		self.fontsize = "15"
		self.term = "epslatex"

		self.xmax = 0
		self.ymax = 0

		self.fit = 1
		self.extra = ""

		self.number = 1



#global variable with all settings, TODO: make local
plot = C_Plot()

# TODO: revise
def loadfile():
	file = open(plot.filename, "r")

	for line in file:
		items = line.rstrip("\n").split(' ')
		items[0] = items[0][0:-1]
		print items
		if items[0] == "x_error":
			plot.xerror = int(items[1])
		elif items[0] == "y_error":
			plot.yerror = int(items[1])
		elif items[0] == "output":
			plot.output = items[1]

		elif items[0] == "x_title":
			plot.xtitle = ' '.join(items[1:])
		elif items[0] == "y_title":
			plot.ytitle = ' '.join(items[1:])
		elif items[0] == "x_limits":
			plot.xlimits = '['+items[1]+':'+items[2]+']'
			plot.xmax = int(items[2])
		elif items[0] == "y_limits":
			plot.ylimits = '['+items[1]+':'+items[2]+']'
			plot.ymax = int(items[2])

		elif items[0] == "label":
			plot.label = items[1]
		elif items[0] == "label_x":
			plot.labelx = items[1]
		elif items[0] == "label_y":
			plot.labely = items[1]
		elif items[0] == "label_text":
			plot.labeltext = ' '.join(items[1:]).strip('"')
		elif items[0] == "font_size":
			plot.fontsize = items[1]
		elif items[0] == "term":
			plot.term = ' '.join(items[1:])


		elif items[0] == "extra":
			plot.extra = plot.extra + ' '.join(items[1:])+'\n'

		elif items[0] == "fit":
			plot.fit = int(items[1])
		elif items[0] == "plots_number":
			plot.number = int(items[1])

		elif items[0] == "data":
			break
		else: 
			pass

	print "SEE", plot.fit
	proceed(file)
	file.close()

# TODO: revise and join with previous
def proceed(file):
	if not plot.output:
		print "Wrong file format"
		sys.exit(1)

	tempfile = open(plot.tempname, "w")
	for line in file:
		if line == '\n' or not line or line[0] == '#':
			pass
		else:
			tempfile.write(line.replace(",", "."))
	
	tempfile.close()

	doplot()


def doplot():
	g = Gnuplot.Gnuplot(debug=1)
	if plot.fit:
		g('f(x)=a*x+b')
# Using of temporary file. TODO.
		g('fit f(x) "'+\
			plot.tempname+\
			'" using 1:2 via a,b')


	g('unset key')
# TODO: just random values. Make settings
	g('set term wxt size 1600,900 font "sansserif, '+\
		plot.fontsize+'"')


	if plot.xtitle:
		g.xlabel(plot.xtitle)
	if plot.ytitle:
		g.ylabel(plot.ytitle)


# TODO: give chance to change style
	g('''

	set style line 1 lc rgb \'black\' pt 7 ps 1.2 lt 5 lw 3
	set style line 2 lc rgb \'black\' pt 7 ps 0 lt 5 lw 1

	set grid ytics lc rgb "#bbbbbb" lw 1 lt 0
	set grid xtics lc rgb "#bbbbbb" lw 1 lt 0
	
	set grid mytics lc rgb "#cccccc" lw 1 lt 0
	set grid mxtics lc rgb "#cccccc" lw 1 lt 0

	set fit errorvariables

	''')
	g(plot.extra)

	if plot.xlimits:
		g('set xrange ' + plot.xlimits)
	if plot.ylimits:
		g('set yrange ' + plot.ylimits)



	if plot.label and plot.fit:
		s = 'set label sprintf('+\
		('"$K = %.2f\\\\pm%.2f$' if plot.term == "epslatex" else '"K = %.2f+-%.2f')+\
		(plot.labeltext if plot.labeltext else "")+\
		'",a, a_err)'



		if plot.labelx and plot.labely:
			s = s+' at '+str(plot.labelx)+','+\
			str(plot.labely)
		else:
			s = s+' at '+str(plot.xmax*0.1)+','+\
			str(plot.ymax*0.9)


		g(s)

	s1 =  ' "' + plot.tempname +'"'
	s = 'plot ' + s1+' using 1:2 ls 1,' + s1


	if plot.xerror and plot.yerror:
		s = s+' using 1:2:4:3 ls 2 with xyerrorbars'
	elif plot.xerror:
		s = s+' using 1:2:3 ls 2 with xerrorbars'
	elif plot.yerror:
		s = s+' using 1:2:3 ls 2 with yerrorbars'
	else:
		s = s+' using 1:2 ls 2 with points'
		
	if plot.fit:
		s = s +	', f(x) ls 1 with lines'

	g(s)

	

	
	g('set output "'+plot.output+'"')

#TODO: just random values for A4 paper LaTeX. Give chance to change.
	if plot.term == "epslatex":
		g('set term epslatex size 16.5cm,10cm')
		g('set format xy "$%g$"')

		#if plot.xscale and plot.yscale:
			#g('set size '+str(plot.xscale)+','+str(plot.yscale))

	else:
		g('set term '+plot.term+' size 1600,900 font "sansserif, '+\
		plot.fontsize+'"')

	g('replot')

	raw_input('')
	os.remove(plot.tempname)



# TODO: everywhere, implement error checks
if __name__ == "__main__":
    if len (sys.argv) == 2:
        plot.filename = sys.argv[1]
        loadfile()
    else:
    	print "Using: __main__ [filename]"
        sys.exit(1)
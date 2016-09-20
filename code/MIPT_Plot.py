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
		self.labelsize = None
		self.term = "epslatex"



#global variable with all settings, TODO: make local
plot = C_Plot()

# TODO: revise
def loadfile():
	file = open(plot.filename, "r")

	for line in file:
		items = line.rstrip("\n").split(' ')
		items[0] = items[0][0:-1]
		#print items
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
		elif items[0] == "y_limits":
			plot.ylimits = '['+items[1]+':'+items[2]+']'

		elif items[0] == "label":
			plot.label = items[1]
		elif items[0] == "label_x":
			plot.labelx = items[1]
		elif items[0] == "label_y":
			plot.labely = items[1]
		elif items[0] == "label_text":
			plot.labeltext = ' '.join(items[1:]).strip('"')
		elif items[0] == "label_size":
			plot.labelsize = items[1]
		
		elif items[0] == "term":
			plot.term = ' '.join(items[1:])

		elif items[0] == "data":
			break
		else: 
			pass


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
	g = Gnuplot.Gnuplot()#debug=1)
	g('f(x)=a*x+b')
# Using of temporary file. TODO.
	g('fit f(x) "'+\
		plot.tempname+\
		'" using 1:2 via a,b')


	g('unset key')
# TODO: just random values. Make settings
	g('set term wxt size 1000,600')



	if plot.xtitle:
		g.xlabel(plot.xtitle)
	if plot.ytitle:
		g.ylabel(plot.ytitle)


# TODO: give chance to change style
	g('set style line 1 lc rgb \'black\' pt 7 ps 2 lt 5 lw 3 # --- blue')
	if plot.label:
		s = 'set label sprintf('+\
		('"$K = %.2f$' if plot.term == "epslatex" else '"K = %.2f')+\
		(plot.labeltext if plot.labeltext else "")+\
		'",a)'+\
			' font "sansserif,'+\
			(str(plot.labelsize) if plot.labelsize else "") +\
			'"'
# Label size doesn't work in LaTeX! TODO.

# TODO: try to do it automatically
		if plot.labelx and plot.labely:
			s = s+' at '+str(plot.labelx)+','+\
			str(plot.labely)
		g(s)


	

	s = 'plot ' + (plot.xlimits if (plot.xlimits) else '') + ' '+\
		(plot.ylimits if (plot.ylimits) else '') +\
		' "' + plot.tempname


	if plot.xerror and plot.yerror:
		print "here"
		s = s+'" using 1:2:4:3 ls 1 with xyerrorbars'
	elif plot.xerror:
		s = s+'" using 1:2:3 ls 1 with xerrorbars'
	elif plot.yerror:
		s = s+'" using 1:2:3 ls 1 with yerrorbars'
	else:
		s = s+'" using 1:2 ls 1 with points'
		

	s = s +	', f(x) ls 1 with lines'

	g(s)

	

	g('set term '+plot.term)
	g('set output "'+plot.output+'"')

#TODO: just random values for A4 paper LaTeX. Give chance to change.
	if plot.term == "epslatex":
		
		g('set format xy "$%g$"')

		if plot.xscale and plot.yscale:
			g('set size '+str(plot.xscale)+','+str(plot.yscale))


	#g('set style line 1 lc rgb \'black\' pt 7 ps 2 lt 5 lw 3 # --- blue')
	

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
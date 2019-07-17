from fpdf import FPDF

class PDFMcTable(FPDF):
	
	def __init__(self, orientation="L"):
		self.cell_widths = []
		self.alignments = []
		self.line_heights = 0
		super(PDFMcTable, self).__init__(orientation=orientation)

	def set_cell_widths(self, cell_widths):
		self.cell_widths = cell_widths

	def set_alignments(self, alignments):
		self.alignments = alignments

	def set_line_heights(self, line_height):
		self.line_height = line_height

	def write_row(self, row_values):
		num_lines = 0

		#find the max lines
		num_of_items = len(row_values)
		for i in range(0, num_of_items):
			num_lines = max(num_lines, self.get_num_lines(self.cell_widths[i], row_values[i]))

		#
		row_height = self.line_height * num_lines

		#page break if needed
		self.check_page_break(row_height)
		#draw the cells
		for i in range(0, num_of_items):
			col_width = self.cell_widths[i]
			#apply alignment
			alignment = "L"
			if self.alignments and self.alignments[i]:
				alignment = self.alignments[i]
			#
			x = self.get_x()
			y = self.get_y()
			# draw the border
			self.rect(x, y, col_width, row_height)
			self.multi_cell(col_width, self.line_height, row_values[i], 0, alignment)
			self.set_xy(x+col_width, y)
		#
		self.ln(row_height)

	def check_page_break(self, height):
		# check height would casuse an overflow
		if self.get_y() + height > self.page_break_trigger:
			self.add_page(self.cur_orientation)

	def get_num_lines(self, width, cell_value):
		#
		cw = self.current_font['cw']
		if width == 0:
			width = self.w - self.r_margin - self.x

		wmax = (width - 2*self.c_margin) * 1000/self.font_size

		stext = cell_value.replace("\r", "")
		nb = len(stext)

		if nb > 0 and stext[nb-1] == "\n":
			nb = nb -1
		
		sep = -1
		i = 0
		j = 0
		l = 0
		num_lines = 1
		while i < nb:
			c = stext[i]
			if c == "\n":
				i = i + 1
				sep = -1
				j = i
				l=0
				num_lines = num_lines + 1
				continue
			#
			if c == ' ':
				sep = i
			l = l + cw[c]
			if l > wmax:
				if sep == -1:
					if i == j:
						i=i+1
				else:
					i = sep + 1
				sep = -1
				j = i
				l = 0
				num_lines = num_lines + 1
			else:
				i = i + 1
		#
		return num_lines

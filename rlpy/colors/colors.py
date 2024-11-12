import numpy as np

from colors import Color
from typing import Sequence


__all__ = ["table1", "table2", "table3"]


table1 = np.array((
	np.array((Color(80, 127, 57), Color(57, 127, 63), Color(57, 127, 100), Color(57, 125, 127), Color(57, 107, 127), Color(57, 93, 127), Color(57, 79, 127), Color(57, 66, 127), Color(76, 57, 127), Color(8, 57, 127))),
	np.array((Color(101, 178, 62), Color(62, 178, 72), Color(62, 178, 134), Color(62, 174, 178), Color(62, 145, 178), Color(62, 122, 178), Color(62, 99, 178), Color(62, 77, 178), Color(93, 62, 178), Color(103, 62, 178))),
	np.array((Color(114, 229, 57), Color(57, 229, 71), Color(57, 229, 163), Color(57, 223, 229), Color(57, 180, 229), Color(57, 146, 229), Color(57, 111, 229), Color(57, 80, 229), Color(103, 57, 229), Color(117, 57, 229))),
	np.array((Color(92, 252, 12), Color(12, 252, 32), Color(12, 252, 160), Color(12, 244, 252), Color(12, 184, 252), Color(12, 136, 252), Color(12, 88, 252), Color(12, 44, 252), Color(76, 12, 252), Color(96, 12, 252))),
	np.array((Color(74, 204, 10), Color(10, 204, 26), Color(10, 204, 129), Color(10, 197, 204), Color(10, 149, 204), Color(10, 110, 204), Color(10, 71, 204), Color(10, 36, 204), Color(61, 10, 204), Color(78, 10, 204))),
	np.array((Color(60, 165, 8), Color(8, 165, 21), Color(8, 165, 105), Color(8, 160, 165), Color(8, 121, 165), Color(8, 89, 165), Color(8, 58, 165), Color(8, 29, 165), Color(50, 8, 165), Color(63, 8, 165))),
	np.array((Color(46, 127, 6), Color(6, 127, 16), Color(6, 127, 81), Color(6, 123, 127), Color(6, 93, 127), Color(6, 68, 127), Color(6, 44, 127), Color(6, 22, 127), Color(38, 6, 127), Color(48, 6, 127)))
))

table2 = np.array((
	np.array((Color(127, 127, 57), Color(127, 112, 57), Color(127, 99, 57), Color(127, 90, 57), Color(127, 84, 57), Color(127, 78, 57), Color(127, 71, 57), Color(127, 57, 57), Color(127, 57, 81), Color(127, 57, 92))),
	np.array((Color(178, 178, 62), Color(178, 153, 62), Color(178, 132, 62), Color(178, 116, 62), Color(178, 106, 62), Color(178, 97, 62), Color(178, 85, 62), Color(178, 62, 62), Color(178, 62, 103), Color(178, 62, 120))),
	np.array((Color(229, 229, 57), Color(229, 192, 57), Color(229, 160, 57), Color(229, 137, 57), Color(229, 123, 57), Color(229, 109, 57), Color(229, 91, 57), Color(229, 57, 57), Color(229, 57, 117), Color(229, 57, 143))),
	np.array((Color(252, 252, 12), Color(252, 200, 12), Color(252, 156, 12), Color(252, 124, 12), Color(252, 104, 12), Color(252, 84, 12), Color(252, 60, 12), Color(252, 12, 12), Color(252, 12, 96), Color(252, 12, 132))),
	np.array((Color(204, 204, 10), Color(204, 162, 10), Color(204, 126, 10), Color(204, 100, 10), Color(204, 84, 10), Color(204, 68, 10), Color(204, 48, 10), Color(204, 10, 10), Color(204, 10, 78), Color(204, 10, 107))),
	np.array((Color(165, 165, 8), Color(165, 131, 8), Color(165, 102, 8), Color(165, 81, 8), Color(165, 68, 8), Color(165, 55, 8), Color(165, 39, 8), Color(165, 8, 8), Color(165, 8, 63), Color(165, 8, 87))),
	np.array((Color(127, 127, 6), Color(127, 101, 6), Color(127, 79, 6), Color(127, 62, 6), Color(127, 52, 6), Color(127, 42, 6), Color(127, 30, 6), Color(127, 6, 6), Color(127, 6, 48), Color(127, 6, 66)))
))

table3 = np.array((
	np.array((Color(229, 229, 229), Color(255, 127, 127), Color(255, 159, 127), Color(255, 207, 127), Color(239, 255, 127), Color(175, 255, 127), Color(127, 255, 127), Color(127, 255, 178), Color(127, 233, 255), Color(127, 176, 255), Color(127, 136, 255), Color(174, 127, 255), Color(229, 127, 255), Color(255, 127, 208), Color(255, 127, 148))),
	np.array((Color(191, 191, 191), Color(255, 89, 89), Color(255, 130, 89), Color(255, 192, 89), Color(234, 255, 89), Color(151, 255, 89), Color(89, 255, 89), Color(89, 255, 155), Color(89, 227, 255), Color(89, 152, 255), Color(89, 100, 255), Color(150, 89, 255), Color(221, 89, 255), Color(255, 89, 194), Color(255, 89, 116))),
	np.array((Color(153, 153, 153), Color(255, 50, 50), Color(255, 101, 50), Color(255, 178, 50), Color(229, 255, 50), Color(127, 255, 50), Color(50, 255, 50), Color(50, 255, 132), Color(50, 220, 255), Color(50, 129, 255), Color(50, 64, 255), Color(125, 50, 255), Color(214, 50, 255), Color(255, 50, 180), Color(255, 50, 85))),
	np.array((Color(102, 102, 102), Color(255, 0, 0), Color(255, 63, 0), Color(255, 159, 0), Color(223, 255, 0), Color(95, 255, 0), Color(0, 255, 0), Color(0, 255, 102), Color(0, 212, 255), Color(0, 97, 255), Color(0, 17, 255), Color(93, 0, 255), Color(204, 0, 255), Color(255, 0, 61), Color(255, 0, 42))),
	np.array((Color(63, 63, 63), Color(178, 0, 0), Color(178, 44, 0), Color(178, 111, 0), Color(156, 178, 0), Color(66, 178, 0), Color(0, 178, 0), Color(0, 178, 71), Color(0, 148, 178), Color(0, 68, 178), Color(0, 11, 178), Color(65, 0, 178), Color(142, 0, 178), Color(178, 0, 113), Color(178, 0, 29))),
	np.array((Color(38, 38, 38), Color(102, 0, 0), Color(102, 25, 0), Color(102, 63, 0), Color(89, 102, 0), Color(38, 102, 0), Color(0, 102, 0), Color(0, 102, 40), Color(0, 84, 102), Color(0, 39, 102), Color(0, 6, 102), Color(37, 0, 102), Color(81, 0, 102), Color(102, 0, 64), Color(102, 0, 17))),
	np.array((Color(0, 0, 0), Color(51, 0, 0), Color(51, 12, 0), Color(51, 31, 0), Color(44, 51, 0), Color(19, 51, 0), Color(0, 51, 0), Color(0, 51, 20), Color(0, 42, 51), Color(0, 19, 51), Color(0, 3, 51), Color(18, 0, 51), Color(40, 0, 51), Color(51, 0, 32), Color(51, 0, 8)))
))


def closest_color(color:Color, colors:Sequence[Sequence[Color]], kl:float=1, kc:float=1, kh:float=1) -> tuple[Color, Sequence[int]]:
	colors_array = np.array(tuple(map(lambda row: tuple(map(lambda c: (c.red, c.green, c.blue), row)), colors)))
	color_row = np.zeros_like(colors_array[0])
	color_row[0] = (color.red, color.green, color.blue)
	colors_array = np.vstack((colors_array, [color_row]))

	del color_row

	# https://stackoverflow.com/a/8433985/11780316

	r = colors_array[:, :, 0] / 255
	g = colors_array[:, :, 1] / 255
	b = colors_array[:, :, 2] / 255

	r = np.power(((r + 0.055) / 1.005), 2.4) if r.any() > 0.04045 else r / 12.92
	g = np.power(((g + 0.055) / 1.005), 2.4) if g.any() > 0.04045 else g / 12.92
	b = np.power(((b + 0.055) / 1.005), 2.4) if b.any() > 0.04045 else b / 12.92

	r, g, b = r * 100, g * 100, b * 100

	X = r * 0.4124 + g * 0.3576 + b * 0.1805
	Y = r * 0.2126 + g * 0.7152 + b * 0.0722
	Z = r * 0.0193 + g * 0.1192 + b * 0.9505

	x, y, z = X / 95.047, Y / 100.000, Z / 108.883

	value = np.divide(16, 116)
	one_third = np.divide(1, 3)
	x = np.power(x, one_third) if x.any() > 0.008856 else ((7.787 * x) + value)
	y = np.power(y, one_third) if y.any() > 0.008856 else ((7.787 * y) + value)
	z = np.power(z, one_third) if z.any() > 0.008856 else ((7.787 * z) + value)

	l = (116 * y) - 16
	a = 500 * (x - y)
	b = 200 * (y - z)

	del r, g, x, y, z, X, Y, Z, value, one_third

	lab = np.array([l[-1, 0], a[-1, 0], b[-1, 0]])
	l1, a1, b1, = np.delete(l, -1, axis=0), np.delete(a, -1, axis=0), np.delete(b, -1, axis=0)
	colors_lab = np.dstack([l1, a1, b1]) # c1
	l2, a2, b2 = lab

	# https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/ciede2000noteCRNA.pdf
	# https://github.com/lovro-i/CIEDE2000/blob/master/ciede2000.py

	C1 = np.sqrt(np.square(a1) + np.square(b1))
	C2 = np.sqrt(np.square(a2) + np.square(b2))
	C_average = np.divide(C1 + C2, 2)
	_C_7 = np.power(C_average, 7)
	_25_7 = np.power(25, 7)
	G = 0.5 * (1 - np.sqrt(np.divide(_C_7, _C_7 + _25_7)))

	_G1 = G + 1
	_a1, _a2 = np.multiply(_G1, a1), np.multiply(_G1, a2)

	_C1 = np.sqrt(np.power(_a1, 2) + np.power(b1, 2))
	_C2 = np.sqrt(np.power(_a2, 2) + np.power(b2, 2))

	_2pi = np.multiply(np.pi, 2)
	_shape = colors_lab.shape[:-1]
	_h1 = np.zeros_like(_shape) if b1.any() == 0 and _a1.any() == 0 else (np.atan2(b1, _a1) if _a1.any() >= 0 else np.atan2(b1, _a1) + _2pi)
	_h2 = np.zeros_like(_shape) if b2.any() == 0 and _a2.any() == 0 else (np.atan2(b2, _a2) if _a2.any() >= 0 else np.atan2(b2, _a2) + _2pi)

	_dL, _dC, _dh = np.subtract(l2, l1), np.subtract(C2, C1), np.subtract(_h2, _h1)

	_C1C2 = np.multiply(_C1, _C2)
	_dh = np.zeros_like(_shape) if _C1C2.any() == 0 else (_dh - _2pi if _dh.any() > np.pi else (_dh + _2pi if _dh.any() < -np.pi else _dh))

	_dH = 2 * np.sqrt(_C1C2) * np.sin(_dh / 2)

	L_average, C_average = np.divide(l1 + l2, 2), np.divide(_C1 + _C2, 2)

	_dh = np.abs(_h1 - _h2)
	_sh = _h1 + _h2
	C1C2 = _C1 + _C2

	_h_ave = (_h1 + _h2) / 2
	C1C20 = (C1C2 != 0).any()
	h_average = _h_ave if all((_dh.any() < np.pi, C1C20)) else (h_ave + _2pi if all((_dh.any() > np.pi, _sh < _2pi, C1C20)) else (_h_ave if all((_dh.any() > np.pi, _sh >= _2pi, C1C20)) else _h1 + _h2))
	del C1C20

	_pi30 = np.divide(np.pi, 30)
	_63pi100 = np.divide(np.multiply(63, np.pi), 100)
	T = 1 - (0.17 * np.cos(h_average - np.divide(np.pi, 6))) + (0.24 * np.cos(2 * h_average)) + (0.32 * np.cos(3 * h_average + _pi30)) - (0.2 * np.cos((4 * h_average) - _63pi100))

	h_average_degree = np.degrees(h_average)
	h_average_degree = h_average_degree + 360 if h_average_degree.any() < 0 else (h_average_degree - 360 if h_average_degree.any() > 360 else h_average_degree)

	dTheta = 30 * np.exp(-np.square((h_average_degree - 275) / 25))

	_C_7 = np.power(C_average, 7)
	R_C = 2 * np.sqrt(np.divide(_C_7, _C_7 + _25_7))
	S_C = 1 + np.multiply(0.045, C_average)
	S_H = 1 + np.multiply(0.015, C_average * T)

	_Lm502 = np.square(L_average - 50)
	S_L = 1 + np.divide(0.015 * _Lm502, np.sqrt(20 + _Lm502))
	R_T = -np.sin(dTheta * np.pi / 90) * R_C

	_fL = _dL / kl / S_L
	_fC = _dC / kc / S_C
	_fH = _dH / kh / S_H

	diff = np.sqrt(np.square(_fL) + np.square(_fC) + np.square(_fH) + R_T * _fC * _fH)
	closest = np.unravel_index(np.argmin(diff, axis=None), diff.shape)
	return colors[closest], closest


if __name__ == "__main__":
	from num2words import num2words
	from sys import argv

	def format_color(color:Color) -> str:
		return f"{color:%fColor(%r, %g, %b, %a)%t}"

	color = Color(rgba=argv[1])
	best, idx = closest_color(color, table3)
	row, col = idx
	col = num2words(col+1, to="ordinal")
	row = num2words(row+1, to="ordinal")

	print(f"The closest color to {format_color(color)} is {format_color(best)} in the {row} row and {col} column.")

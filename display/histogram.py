import copy

def histogramString(inputString, outputString):

  def _makeChart():
    bar_chart_string = ""
    line = 0
    for percent in range(110, 10, -10):
      if percent == 110:
        bar_chart_string += " %  |"
      else:
        bar_chart_string += "{:>3d}-|".format(percent)
      bar_chart_string += _getChartLine(input_dict, line)
      bar_chart_string += ' '
      if percent == 110:
        bar_chart_string += " %  |"
      else:
        bar_chart_string += "{:>3d}-|".format(percent)
      bar_chart_string += _getChartLine(output_dict, line)
      bar_chart_string += '\n'
      line += 1
    for percent in range(10, 0, -1):
      bar_chart_string += "{:>3d}-|".format(percent)
      bar_chart_string += _getChartLine(input_dict, line)
      bar_chart_string += ' '
      bar_chart_string += "{:>3d}-|".format(percent)
      bar_chart_string += _getChartLine(output_dict, line)
      bar_chart_string += '\n'
      line += 1
    for line in range(20, 28):
      if line in [21,22,23,24,26,27]:
        bar_chart_string += "    |"
      elif line in [20]:
        bar_chart_string += "  0-|"
      elif line in [25]:
        bar_chart_string += "  % |"
      bar_chart_string += _getChartLine(input_dict, line)
      if line in [21,22,23,24,26,27]:
        bar_chart_string += "     |"
      elif line in [20]:
        bar_chart_string += "   0-|"
      elif line in [25]:
        bar_chart_string += "   % |"
      bar_chart_string += _getChartLine(output_dict, line)
      bar_chart_string += '\n'
    bar_chart_string += "    {0}     {1}".format('-' * 37, '-' * 27)
    bar_chart_string += "\n     VALID INPUT CHARACTER DISTRIBUTION       ENIGMA OUTPUT DISTRIBUTION"
    bar_chart_string += "\n\n    : -> greater than half the percentage increment"
    bar_chart_string += "\n    . -> less than or equal to half the percentage increment"
    bar_chart_string += "\n    ~ -> Character used but may be to small to register as a %"

    return bar_chart_string

  def _getChartLine(_dict, line):
    chart_line = ""
    for char in _dict:
      if char.isalpha():
        chart_line += _dict[char][2][line]
    for char in _dict:
      if char.isdigit():
        chart_line += _dict[char][2][line]
    return chart_line

  def _makeBarChartStrings(_dict):
    for char in _dict:
      percent = _dict[char][1]
      string = ""
      if percent > 0:
        string = char
      if percent >= 10:
        if percent - int(percent) <= 5 and percent - int(percent) != 0:
          string += '.'
        elif percent - int(percent) > 5:
          string += ':'
        string += "{}".format('*' * int((int(percent)/10 + 9)))
      elif percent < 10:
        if float(percent - int(percent)) <= 0.5 and float(percent - int(percent)) >= 0.1:
          string += '.'
        elif float(percent - int(percent)) > 0.5 :
          string += ':'
        if percent < 0.1 and percent > 0:
          string += '~'
        string += "{}".format('*' * int(percent))
      string = "{:>20s}".format(string)
      string += "-{0}|{1:0>5.1f}".format(char, float(percent))
      _dict[char][2] = string
    return _dict

  def _countInputChars(input_string, input_dict):
    for char in input_string:
      if char in input_dict:
        input_dict[char][0] += 1
        nonlocal total_input_count
        total_input_count += 1
      else:
        raise ValueError(f"{char} is not a valid input character")
    return input_dict

  def _countOutputChars(output_string, output_dict):
    for char in output_string:
      if char in output_dict:
        output_dict[char][0] += 1
        nonlocal total_output_count
        total_output_count += 1
      else:
        raise ValueError(f"{char} is not a valid output character")
    return output_dict

  def _calculateInputPercentages():
    return _calculatePercentages(input_dict, total_input_count)

  def _calculateOutputPercentages():
    return _calculatePercentages(output_dict, total_output_count)

  def _calculatePercentages(_dict, total):
    for char in _dict:
      char_count = _dict[char][0]
      percentage = 0.0
      try:
        percentage = (float(char_count)/total) * 100
      except ZeroDivisionError:
        pass
      else:
        _dict[char][1] = percentage
    return _dict

  lets = {chr(i):[0, 0, ""] for i in range(65,91)}
  nums = {chr(i):[0, 0, ""] for i in range(48,58)}
  input_dict = copy.deepcopy({**lets,**nums})
  output_dict = lets
  total_input_count = 0
  total_output_count = 0
  input_dict = _countInputChars(inputString, input_dict)
  output_dict = _countOutputChars(outputString, output_dict)
  input_dict = _calculateInputPercentages()
  output_dict = _calculateOutputPercentages()
  input_dict = _makeBarChartStrings(input_dict)
  output_dict = _makeBarChartStrings(output_dict)
  chart = _makeChart()
  return chart
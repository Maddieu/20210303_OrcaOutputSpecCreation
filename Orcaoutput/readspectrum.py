def readspectrum(content):

    tempspec = []
    for n, line in enumerate(content):
        if line.startswith('         ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS'):
            break
    for m, line in enumerate(content[n::]):
        if line == "\n":
            break
        else:
            if line.split()[0].isnumeric():
                tempspec.append(line)
            #print(line, end="")

    spectrumdictionary = {}

    spectrumdictionary['Energy'] = [round(float(i.split()[1])*0.000123984193,4) for i in tempspec]
    spectrumdictionary['Intensity'] = [round(float(i.split()[3]),9) for i in tempspec]
    spectrumdictionary['Index'] = [round(float(i.split()[0])) for i in tempspec]
    return spectrumdictionary





def readcontributions(content):
    temptransitions = []
    for n, line in enumerate(content):
        if line.startswith('TD-DFT/TDA EXCITED STATES'):
            break
    for m, line in enumerate(content[n+5::]):
        if line.startswith('-----'):
            break
        else:
            temptransitions.append(line)
            #print(line, end="")

    transitionsdictionary = {}

    for n, line in enumerate(temptransitions):
        if line.startswith('STATE'):
            statenumber = int(line.split()[1].replace(':',''))
            startline = n
        if line == "\n":
            transitionsdictionary[statenumber] = temptransitions[startline:n]

    #print('debug 1:', transitionsdictionary[1])
    return transitionsdictionary
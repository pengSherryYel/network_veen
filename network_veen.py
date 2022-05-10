import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import os,argparse

parser = argparse.ArgumentParser(description='network veen')
##required
parser.add_argument("-e",type=str,required=True,help="edge_profile. header must same with example/edge_file.txt")
parser.add_argument("-n",type=str,required=True,help="node_profile. header must same with example/node_file.txt")
##optional
parser.add_argument("-o",type=str,help="output image",default="./output.network_veen.pdf")
parser.add_argument("--title",type=str,help="title of output image",default="network_veen")
parser.add_argument("--xlable",type=str,help="xlable of output image",default="")
parser.add_argument("--ylable",type=str,help="ylable of output image",default="")

args = parser.parse_args()


##-----------------------------
## load data
##-----------------------------


edge_file = args.e
node_file = args.n

#edge_file = "./edge_file.txt"
#node_file = "./node_file.txt"
edged = pd.read_csv(edge_file,header=0)
noded = pd.read_csv(node_file,header=0)


##-----------------------------
## run network
##-----------------------------
G = nx.Graph()

for i in edged.index:
    G.add_edge(edged.loc[i,"n1"],edged.loc[i,"n2"],
               weight=int(edged.loc[i,"weight"]),
               color=edged.loc[i,"weigth_color"])

edges = G.edges()
weights = [G[u][v]['weight'] for u,v in edges]
colors = [G[u][v]['color'] for u,v in edges]

##-----------------------------
##change axes str to int
##-----------------------------
posD = {}
## change string to int value
xstep = 2
ystep = 1
x_label = sorted(set(noded.x))
y_label = sorted(set(noded.y))

##this is for change str to int pos
x_label_int={value:index*xstep for index,value in enumerate(x_label)}
y_label_int={value:index*ystep for index,value in enumerate(y_label)}

##this is for set the display label 
x_label_int2str={index*xstep:value for index,value in enumerate(x_label)}
y_label_int2str={index*ystep:value for index,value in enumerate(y_label)}

x_lim_value = (len(x_label) - 1)* xstep + 1
y_lim_value = (len(y_label) - 1)* ystep + 1

min_value=-1
x_label_str = [x_label_int2str[x] if x in x_label_int2str else "" for x in range(min_value, x_lim_value + 1)]
y_label_str = [y_label_int2str[y] if y in y_label_int2str else "" for y in range(min_value, y_lim_value + 1)]

x_label_integer = [x for x in range(min_value, x_lim_value + 1)]
y_label_integer = [x for x in range(min_value, y_lim_value + 1)]
        
print(x_label_str,y_label_str)
print(x_label_integer, y_label_integer)
print(x_lim_value,y_lim_value)

## form the pos dict
for i in noded.index:
    posD[noded.loc[i,"n"]] = [x_label_int[noded.loc[i,"x"]],
                              y_label_int[noded.loc[i,"y"]]]
    
print(posD)

##-----------------------------
## plot net work
##-----------------------------

nx.draw(G, posD, 
        node_size=noded["size"]*200, 
        nodelist=noded["n"] , 
        node_color = noded.node_color,
        edgecolors = "black",
#         with_labels=True, font_size = 10,
        width=weights,
        edge_color = colors)

## set axes
ax = plt.gca()
ax.margins(0.20)

plt.axis("on")
ax.set_title(args.title)
plt.xlabel(args.xlable)
plt.ylabel(args.ylable)

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

## set int to str axes
ax.set_xlim(min_value,x_lim_value)
plt.xticks(x_label_integer)
ticks_loc = ax.get_xticks().tolist()
ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax.set_xticklabels(x_label_str)


ax.set_ylim(min_value,y_lim_value)
plt.yticks(y_label_integer)
yticks_loc = ax.get_yticks().tolist()
ax.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax.set_yticklabels(y_label_str)


plt.savefig(args.o,dpi=300, bbox_inches='tight')


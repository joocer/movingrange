

def plot_waterfall_chart(series):

    from matplotlib.patches import Rectangle
    from matplotlib import pyplot as plt

    plt.figure(figsize=(20, 6))
    plt.ylim(0, 1+(max(series)//1))
    plt.xlim(0, len(series))

    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    m = max(series)

    col = 0
    last_item = 0
    for item in series:
        
        if item > last_item:
            color = "#32ab60"
        if item < last_item:
            color = "#db4052"
        if item == last_item:
            color = "#00bfff"
            
        plt.gca().add_patch(Rectangle((col+0.1,last_item),0.9,item - last_item,linewidth=2,edgecolor=color,facecolor=color))
        
        col += 1
        last_item = item
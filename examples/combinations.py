from visualiser.visualiser import Visualiser as vs

st= []
@vs(show_argument_name=False, node_properties_kwargs={"shape":"record", "color":"#f57542", "style":"filled", "fillcolor":"grey"})
def combi(prefix, s):
    if len(s) == 0:
        return " "
    else:
        st.append(prefix + s[0])
        combi(prefix=prefix + s[0], s=s[1:])
        combi(prefix=prefix, s=s[1:])
        return st

print(combi(prefix="",s='abc'))
vs.make_animation("combinations.gif", delay=3)
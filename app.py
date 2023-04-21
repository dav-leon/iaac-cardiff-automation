# import flask, ghhops_server, and rhino3dm
# rhino3dm is automatically installed with ghhops_server
from flask import Flask
import ghhops_server as hs
import rhino3dm

# register hops app as middleware
app = Flask(__name__)
hops = hs.Hops(app)

@hops.component(
    "/pointat",
    name="PointAt",
    description="Get point along curve",
    icon="examples/pointat.png",
    inputs=[
        hs.HopsCurve("Curve", "C", "Curve to evaluate"),
        hs.HopsNumber("t", "t", "Parameter on Curve to evaluate"),
    ],
    outputs=[
        hs.HopsPoint("P", "P", "Point on curve at t")
    ]
)
def pointat(curve, t):
    return curve.PointAt(t)


import meshutils as mu

@hops.component(
    "/meshwalker",
    name = "meshwalker",
    inputs=[
        hs.HopsMesh("Input Mesh", "M", "Mesh"),
        hs.HopsInteger("Source", "S", "Source Vertex"),
        hs.HopsInteger("Target", "T", "Target Vertex"),


    ],
    outputs=[
        hs.HopsString("text","T","Graph string" ),
        hs.HopsInteger("ShortestPath","SP","shortest path points", hs.HopsParamAccess.LIST )


    ]
)
def meshToGraph(mesh, source, target):

    G = mu.SimpleGraphFromMesh(mesh)
    
    sp = mu.graphShortestPath(G, source, target)
    print(sp)

    return str(G), sp




if __name__ == "__main__":
    app.run(debug=True)
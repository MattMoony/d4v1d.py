window.onload = () => {
    let netw = document.getElementById('network');

    let data = {
        nodes: new vis.DataSet(raw_data.nodes),
        edges: new vis.DataSet(raw_data.edges),
    }, opts = {
        physics: {
            adaptiveTimestep: true,
            barnesHut: {
                gravitationalConstant: -8000,
                springConstant: 0.04,
                springLength: 95
            },
            stabilization: {
                iterations: 987
            }
        },
        layout: {
            randomSeed: 191006,
            improvedLayout: true
        }
    };
    let network = new vis.Network(netw, data, opts);

    window.onresize = () => {
        netw.style.width = window.innerWidth - 5 + 'px';
        netw.style.height = window.innerHeight - 5 + 'px';
    };
    window.onresize();
};
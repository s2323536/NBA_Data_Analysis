from flask import Flask,request,render_template,jsonify,session
import pandas as pd
from pymongo import MongoClient
# import certifi

# ca = certifi.where()

client = MongoClient("mongodb://root:123@cluster0-shard-00-00.at4fd.mongodb.net:27017,cluster0-shard-00-01.at4fd.mongodb.net:27017,cluster0-shard-00-02.at4fd.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-ekqzsj-shard-0&authSource=admin&retryWrites=true&w=majority")#, tlsCAFile=ca)
# client = MongoClient("mongodb://root:123@cluster0-shard-00-00.at4fd.mongodb.net:27017,cluster0-shard-00-01.at4fd.mongodb.net:27017,cluster0-shard-00-02.at4fd.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-ekqzsj-shard-0&authSource=admin&retryWrites=true&w=majority", tlsCAFile=ca)


app = Flask(
    __name__,
    static_folder='static',
    static_url_path='/'
)
app.secret_key="any string but secret"
def logo(tid):
    switcher = {
        1610612737:'/AtlantaHawks.png',
        1610612738:'/BostonCeltics.png',
        1610612739:'/ClevelandCavaliers.png',
        1610612740:'/NewOrleansPelicans.png',
        1610612741:'/ChicagoBulls.png',
        1610612742:'/DallasMavericks.png',
        1610612743:'/DenverNuggets.png',
        1610612744:'/GoldenStateWarriors.png',
        1610612745:'/HoustonRockets.png',
        1610612746:'/LAClippers.png',
        1610612747:'/LosAngelesLakers.png',
        1610612748:'/MiamiHeat.png',
        1610612749:'/MilwaukeeBucks.png',
        1610612750:'/MinnesotaTimberwolves.png',
        1610612751:'/BrooklynNets.png',
        1610612752:'/NewYorkKnicks.png',
        1610612753:'/OrlandoMagic.png',
        1610612754:'/IndianaPacers.png',
        1610612755:'/Philadelphia76ers.png',
        1610612756:'/PhoenixSuns.png',
        1610612757:'/PortlandTrail Blazers.png',
        1610612758:'/SacramentoKings.png',
        1610612759:'/SanAntonioSpurs.png',
        1610612760:'/OklahomaCityThunder.png',
        1610612761:'/TorontoRaptors.png',
        1610612762:'/UtahJazz.png',
        1610612763:'/MemphisGrizzlies.png',
        1610612764:'/WashingtonWizards.png',
        1610612765:'/DetroitPistons.png',
        1610612766:'/CharlotteHornets.png'
    }
    return switcher.get(tid)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/ppt1')
def ppt1():
    return render_template('ppt.html')
@app.route('/ppt2')
def ppt2():
    return render_template('ppt2.html')
@app.route('/link')
def link():
    return render_template('link.html')
@app.route('/chart')
def chart():
    SEASON = request.args.get('s',0)
    TEAM_ID = request.args.get('t',0)
    TEAM_ID2 = request.args.get('t2',0)
    g1 = logo(int(TEAM_ID))
    g2 = logo(int(TEAM_ID2))
    return render_template('chart.html', s=SEASON,t=TEAM_ID,t2=TEAM_ID2,g1=g1,g2=g2)

@app.route('/data')
def data():
    SEASON = request.args.get('s')
    TEAM_ID = request.args.get('t')
    result = client['NBA2']['radar'].find({'SEASON':int(SEASON),'TEAM_ID':int(TEAM_ID)},{'_id':0})
    t = pd.DataFrame(list(result))
    t = t.T
    t = t.reset_index()
    t = t.set_axis(['axis','value'],axis=1)
    t = t.loc[2:7,:]
    return jsonify([t.to_dict('records')])

@app.route('/data2')
def data2():
    SEASON = request.args.get('s')
    TEAM_ID = request.args.get('t')
    result = client['NBA2']['elo_eff'].aggregate([
        {'$match':{'SEASON':int(SEASON),'TEAM_ID':int(TEAM_ID)}},
        {'$sort':{'GAME_DATE_EST':1}},
        {'$project':{'SEASON':0,'TEAM_ID':0}},
        {'$project':{'_id':0}}
    ])
    t = pd.DataFrame(list(result))
    t.GAME_DATE_EST = t.GAME_DATE_EST.dt.strftime('%Y-%m-%d')
    t.ELO = t.ELO.astype(int)
    t.EFF = t.EFF.astype(int)
    t.WIN_PR = (t.WIN_PR * 10).round(2)
    return jsonify(t.to_dict('records'))

@app.route('/line')
def line():
    return render_template('line.html')

if __name__ == "__main__":
    app.run(debug=False)   



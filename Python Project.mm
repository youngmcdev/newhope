<map version="freeplane 1.8.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="Python Project" FOLDED="false" ID="ID_1978471855" CREATED="1617224207017" MODIFIED="1617224216396" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle" background="#3c3f41" zoom="1.331">
    <properties fit_to_viewport="false" edgeColorConfiguration="#808080ff,#00ddddff,#dddd00ff,#dd0000ff,#00dd00ff,#dd0000ff,#7cddddff,#dddd7cff,#dd7cddff,#7cdd7cff,#dd7c7cff,#7c7cddff"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24.0 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ICON_SIZE="12.0 pt" COLOR="#cccccc" STYLE="fork">
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#cccccc" BACKGROUND_COLOR="#3c3f41" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important">
<icon BUILTIN="yes"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#dddddd" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10.0 pt" SHAPE_VERTICAL_MARGIN="10.0 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#ff3300">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#ffb439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#99ffff">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#bbbbbb">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="6" RULE="ON_BRANCH_CREATION"/>
<node TEXT="Help" POSITION="right" ID="ID_266016219" CREATED="1617228196120" MODIFIED="1617228199995">
<edge COLOR="#dd0000"/>
<node TEXT="Using the tutorial at" ID="ID_795589106" CREATED="1617227405007" MODIFIED="1617228202790">
<node TEXT="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world" ID="ID_237851357" CREATED="1617227431062" MODIFIED="1617227432873"/>
</node>
<node TEXT="gitignore file" ID="ID_1762526631" CREATED="1617228203992" MODIFIED="1617228210466">
<node TEXT="https://github.com/github/gitignore/blob/master/Python.gitignore" ID="ID_1167572110" CREATED="1617228210648" MODIFIED="1617228212370"/>
</node>
</node>
<node TEXT="Install Flask" POSITION="right" ID="ID_1005278405" CREATED="1617224246703" MODIFIED="1617224260882">
<edge COLOR="#00dddd"/>
<node TEXT="Create a  directory for the project, say /newhope, and enter it." ID="ID_1582181086" CREATED="1617224546616" MODIFIED="1617224724836"/>
<node TEXT="Setup a virtual environment" ID="ID_582604268" CREATED="1617224760105" MODIFIED="1617224771715">
<node TEXT="Command to create it" ID="ID_849129352" CREATED="1617225147474" MODIFIED="1617225168531">
<node TEXT="python3 -m venv venv" ID="ID_1594492493" CREATED="1617224771993" MODIFIED="1617225054383"/>
<node TEXT="This is asking Python to run the venv package, which creates a virtual environment named venv. The first venv in the command is the name of the Python virtual environment package, and the second is the virtual environment name that I&apos;m going to use for this particular environment." ID="ID_1586592098" CREATED="1617224887137" MODIFIED="1617224891524"/>
</node>
<node TEXT="Command to activate it" ID="ID_816442650" CREATED="1617225000962" MODIFIED="1617225184987">
<node TEXT="venv\Scripts\activate" ID="ID_196965525" CREATED="1617225185570" MODIFIED="1617225265940">
<node TEXT="Windows" ID="ID_155253973" CREATED="1617225270193" MODIFIED="1617225273659"/>
</node>
<node TEXT="source venv/bin/activate" ID="ID_1530176385" CREATED="1617225274921" MODIFIED="1617225289596">
<node TEXT="Linux" ID="ID_3839359" CREATED="1617225289738" MODIFIED="1617225291676"/>
</node>
<node TEXT="Now your terminal session is modified so that the Python interpreter stored inside the virtual environment is the one that is invoked when you type python." ID="ID_996486421" CREATED="1617225319250" MODIFIED="1617225359581"/>
</node>
<node TEXT="Command to install Flask in the virtual environment" ID="ID_115332309" CREATED="1617225371755" MODIFIED="1617225382484">
<node TEXT="pip install flask" ID="ID_351511654" CREATED="1617225382610" MODIFIED="1617225393781"/>
<node TEXT="Test by starting the python interpreter and executing" ID="ID_1503651206" CREATED="1617225409291" MODIFIED="1617225433508">
<node TEXT="import flask" ID="ID_1350168114" CREATED="1617225434282" MODIFIED="1617225441068"/>
<node TEXT="Should get no errors" ID="ID_1152284822" CREATED="1617225447362" MODIFIED="1617225451869"/>
</node>
</node>
<node TEXT="Command to install Stripe in the virtual environment" ID="ID_1587192533" CREATED="1618143313015" MODIFIED="1618143332627">
<node TEXT="pip install --upgrade stripe" ID="ID_58769164" CREATED="1618145687959" MODIFIED="1618145690018"/>
</node>
</node>
</node>
<node TEXT="Create application" POSITION="right" ID="ID_1583674960" CREATED="1617227487671" MODIFIED="1617227495570">
<edge COLOR="#dd0000"/>
<node TEXT="Application is named &quot;newhope&quot;. Main file is newhope.py" ID="ID_1874931876" CREATED="1617227599191" MODIFIED="1617227619194"/>
</node>
<node TEXT="Prepare to run application" POSITION="right" ID="ID_1984206254" CREATED="1617227495791" MODIFIED="1617227507993">
<edge COLOR="#00dd00"/>
<node TEXT="Command to set the FLASK_APP environment variable" ID="ID_1441932593" CREATED="1617227544439" MODIFIED="1617227564609">
<node TEXT="set FLASK_APP=newhope.py" ID="ID_65316003" CREATED="1617227570630" MODIFIED="1617227654441">
<node TEXT="Windows" ID="ID_845749544" CREATED="1617227644127" MODIFIED="1617227646297"/>
</node>
<node TEXT="export FLASK_APP=newhope.py" ID="ID_1625830454" CREATED="1617227570630" MODIFIED="1617227591753">
<node TEXT="Linux" ID="ID_335687250" CREATED="1617227640167" MODIFIED="1617227642793"/>
</node>
<node TEXT="Using the python-dotenv package allows for having environment variables in the file, .flaskenv" ID="ID_843980453" CREATED="1617228503337" MODIFIED="1617228560004">
<node TEXT="pip install python-dotenv" ID="ID_840671583" CREATED="1617228560961" MODIFIED="1617228564483"/>
<node TEXT="Add, FLASK_APP=newhope.py, to the file" ID="ID_269234680" CREATED="1617228587089" MODIFIED="1617228686742"/>
</node>
</node>
<node TEXT="Command to run the application" ID="ID_1313929014" CREATED="1617227671487" MODIFIED="1617227677827">
<node TEXT="flask run" ID="ID_356440155" CREATED="1617227678030" MODIFIED="1617227682625"/>
</node>
</node>
<node TEXT="Stripe" POSITION="left" ID="ID_1098002789" CREATED="1618190064617" MODIFIED="1618190069133">
<edge COLOR="#7cdddd"/>
<node TEXT="Tutorials done" ID="ID_889033236" CREATED="1618190071136" MODIFIED="1618190079059">
<node TEXT="https://stripe.com/docs/payments/integration-builder" ID="ID_1818255293" CREATED="1618190134217" MODIFIED="1618190155515">
<icon BUILTIN="button_ok"/>
</node>
<node TEXT="https://stripe.com/docs/payments/accept-a-payment?ui=checkout" ID="ID_1105257330" CREATED="1618190096612" MODIFIED="1618190104765">
<icon BUILTIN="button_ok"/>
</node>
<node TEXT="https://stripe.com/docs/payments/accept-a-payment?ui=elements" ID="ID_1105326381" CREATED="1618190081153" MODIFIED="1618190083516"/>
</node>
</node>
</node>
</map>

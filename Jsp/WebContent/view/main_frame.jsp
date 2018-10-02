<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
<title>대한민국 유기동물 보고서</title>
<!-- 메인프레임 스타일, layout  -->
<style>
	#wrap_css{<!--전체공간여백-->

 
	}
	
	#top {
		background-color:brown;
		height:80px;
		margin:0px 0px 0px 0px;
	}
	
	#graph_line{
		width:100%;
		height:100%;
		}
	
	#graph_line #graph_count{
		background-color:green;
		width:70%;
		height:150px;
		float: left;
	
		}
	
	
	#graph_line #count_animal{
		background-color:pink;
		height:150px;
		width:30%;
		float: left;
	
	}
	
	#graph_line #geo_distribute{
		background-color:pink;
		height:auto;
		width:50%;
		float: left;
	}
	#graph_line #geo_distribute_value{
		background-color:purple;
		height:;
		width:20%;
		float: left;
	}
	
	#graph_line #news{
		
		height:auto;
		width:30%;
		float: left;
	}
</style>
<!-- 메인프레임 스타일, layout end  -->

<!-- 그래프스타일 -->
<style>
#count_animal #yesterday_count{
		background-color:pink;
		height:150px;
		width:100%;
		float: left;
	
	}
#graph_count #total_realtime_graph{
		width:100%;
		
	}
#graph_line #geo_distribute #geograph_distribute{
		background-color:pink;
		height:auto;
		width:100%;
		float: left;
	}
#graph_line #geo_distribute_value #geograph_distribute{
		background-color:purple;
		height:;
		width:100%;
		float: left;
	}
#graph_line #news #animal_news{
		
		height:auto;
		width:100%;
		float: left;
	}		
</style> 
<!-- 그래프스타일 end -->

<!-- 메뉴스타일 -->
<style>
#menubar {
		background-color:yellow;
		height:50px;
		margin:0px 0px 0px 0px;
		

		}
#menubar ul {
		margin: 0px 20px 0px 0px;
		padding: 15px 20px 0px 20px;
		list-style-type:none;	
		
		
	
		}
#menubar ul li{
		padding: 15px 0px 0px 15px;
		display:inline;
		<!--border-left: 1px solid #c0c0c0;-->
			
		}		
</style>
<!-- 메뉴스타일 -->

</head>


	<body>
		<div id='wrap_css'><!-- 전체를 싸고있는 css -->
			<!-- header 부분 -->
			<div id='top'><h2 align="center"> <!--header부분 -->
				<br>대한민국 유기동물 보고서</h2>
			</div>
			<!-- header end-->
			
			<!-- menu -->
			<div id='menubar'>
			<ul>
				<li><a href="main_frame.jsp">메인페이지</a><li>
				<li><a href="./r_frame.jsp" target='graph_line'>통계분석</a><li>
				<li><a href="">머신러닝</a><li>
			</ul>
			</div>
			<!-- menu end-->
			
			
			<div id='graph_line'>
				<div id='graph_count'><iframe id='total_realtime_graph' frameborder='1' src=./main_function/main_total_year_count.jsp></iframe></div>
				<div id='count_animal'><iframe id='yesterday_count' frameborder='1' src='./main_function/Yesterday_count.jsp'><h2 align="center">카운트그래프</h2></iframe></div>	
				<div id='geo_distribute'><iframe id='geograph_distribute' frameborder='1' src=./main_function/main_geograph_distribute.jsp><h2 align="center">지오그래프</h2></iframe></div>
				<div id='geo_distribute_value'><iframe id='geograph_distribute' frameborder="1" src='./main_function/main_geograph_valuecount.jsp'><h2 align="center">지오그래프_value</h2></iframe></div>
				<div id='news'><iframe id='animal_news' src="./main_function/main_news.jsp"><h2 align="center">news</h2></iframe></div>
			</div>
		
		</div>
		
	</body>
	
</html>
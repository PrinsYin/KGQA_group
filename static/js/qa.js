$(document).ready(
function initsvg() {

    // $("#btn1").click(
    //     function()
    //     {
    //         var data={
    //             'name':'kikay',
    //             'age':18
    //         }
    //         console.log("ajax")
    //         $.ajax({
    //             type:'GET',
    //             url:'{{url_for("app.test_get")}}',
    //             data:data,
    //             dataType:'json',//希望服务器返回json格式的数据
    //             success:
    //             function(data){
    //                 console.log(JSON.stringify(data));
    //                 console.log(data['test'])
    //             }
    //         });
    //     }
    // )
    // 定义svg变量，选出第一个图
    var svg = d3.select("#svg1"), 
              width = document.getElementById("svg1").clientWidth*1,
              height = document.getElementById("svg1").clientHeight*1
    console.log(document.getElementById("svg1").clientHeight)
    var colors = ['#005CAF', '#A5DEE4', '#B28FCE'];
//    var outlier_avatar_ID = ['0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0177', '0377', '0378', '0659'];


    var help = ['小助手', '1.开始如果没有节点和边的网状可视化显示，刷新便可出现', '2.鼠标放置在任意节点上，出现和此节点相关的所有节点及之间的关系，右侧自动呈现菜品相关信息', '3.搜索框中输入菜品名称，呈现此菜品所有相关节点，并且此时鼠标位于某个节点上方时移开鼠标能够保持知识图谱当前状态', '4.模式切换按钮可切换对节点的不同可视化表示，Circles为点，Texts为文字', '5.左侧不同颜色的条形表示不同类型的节点，On/Off切换开关可打开或关闭同样类型所有节点的可视化显示'];
    $('#tips').append("<div><span>" + help[0] + "</span></div>")
    for (var i = 1; i < help.length; i++) {
        // 选中indicator，每一种都append一个div，就是前面的小色块
        $('#tips').append("<div>" + help[i] +"</div>")
    }

    // 定义D3的simulation是如何展示出来的
    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) {
            return d.id;
        }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width*5 , height*5));

    // 存之后生成的关系图数据
    var graph;

    d3.json("https://raw.githubusercontent.com/PrinsYin/KGQA/main/vizdata.json", function(error, data) {
        if (error) throw error;
        graph = data;


        // D3数据驱动文档
        // 用links去驱动line的线宽
        var link = svg.append('g')
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .style("color","red")
            .attr('stroke-width', function(d){
            // return Math.sqrt(d.value);
            return 2;//连线宽度
            });

        //边上的文字（实体之间的关系） 
        var linktext = svg.append('g')
            .attr("class", "linetexts")
            .selectAll("text")
            .data(graph.links)
            .enter()
            .append("text")
            .style("display","block")
            .style("color","red")
            .text(function(d){
                return d.relation;
            })
            .attr('fill', "black");//边上字颜色

        // 添加所有的node
        var node = svg.append('g')
            .attr('class', 'nodes')
            .selectAll('circle')
            .data(graph.nodes)
            .enter().append('circle')
            .attr("r", function(d) {
                return d.size
            })
            .attr('fill', function(d){ // 填充的颜色
                return colors[d.group];
            })
            .attr('stroke', 'none')    // 没有描边
            .attr('name', function(d){
                return d.id;
            })
            .attr('namee',function(d){
                return d.class;
            })
            .call(d3.drag()             // 绑定d3的拖动函数
                .on("start", dragstarted) // 拖动开始
                .on("drag", dragged)      // 拖动进行
                .on("end", dragended));   // 拖动结束

        // 文本
        // 两种显示模式，每个结点可以用一个圆或者文本表示
        var text = svg.append('g')
            .attr("class", "texts")
            .selectAll("text")
            .data(graph.nodes)
            .enter().append("text")
            .attr("font-size", function(d) {
                return d.size
            })
            .attr("fill", function(d) {
                return colors[d.group];
            })
            .attr('name', function(d) {
                return d.id;
            })
            .text(function(d) {
                return d.id;
            })
            .attr('text-anchor', 'middle')
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        // 给node加title, 当鼠标悬浮在圆圈上的时候
        node.append('title').text(function(d){
            return d.id;
        })

        // 处理缩放
        svg.call(d3.zoom()
            .scaleExtent([1 / 8, 8])
            .on("zoom", zoomed));
         
        function zoomed() {
            link.attr("transform", d3.event.transform);
            node.attr("transform", d3.event.transform);
            text.attr("transform", d3.event.transform);
            linktext.attr('transform', d3.event.transform);
        }

        simulation
            .nodes(graph.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(graph.links);

        function ticked() {
            link
                .attr("x1", function(d) {
                    return d.source.x;
                })
                .attr("y1", function(d) {
                    return d.source.y;
                })
                .attr("x2", function(d) {
                    return d.target.x;
                })
                .attr("y2", function(d) {
                    return d.target.y;
                });

            linktext.attr("dx",function(d){ return (d.source.x + d.target.x) / 2 ; });
            linktext.attr("dy",function(d){ return (d.source.y + d.target.y) / 2 ; });

            node
                .attr("cx", function(d) {
                    return d.x;
                })
                .attr("cy", function(d) {
                    return d.y;
                });

            text
                .attr("dx", function(d) {
                    return d.x;
                })
                .attr("dy", function(d) {
                    return d.y;
                });
        }
    })

    // 拖动事件函数
    var dragging = false;

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
        dragging = true;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
        dragging = false;
    }

    // 处理模式点击后的事件(这些元素页面上本来有)
    $('#mode span').click(function(event) {
        // 把mode里面所有span的active全部去掉
        // 把被点击的这个设置为active
        $('#mode span').removeClass('active')
        $(this).addClass('active')

        if ($(this).text() == 'Circles') {
            // 隐藏所有文本里面的svg元素
            // 把node里面的显示出来
            $('.texts text').hide();
            $('.nodes circle').show();
        }
        else {
            $('.texts text').show();
            $('.nodes circle').hide ();
        }
    });

    // // 三个开关标志，True表示打开
    // var sw1 = true;
    // var sw2 = true;
    // var sw3 = true;
    // 处理事件：选中结点后只显示选中点及其直接相邻点
    // 这些元素原来没有，后面添加上去，所以写法和上面不同
    // 为#svg1中所有的 `.nodes circle` 元素，绑定了 `mouseenter`事件 
    $('#svg1').on('mouseenter', '.nodes circle', function(event) {
        // 拖动的时候，如果碰到别的结点，效果会发生变化，看起来很乱
        // 所以拖动的时候不允许触发鼠标进入事件
        if (!dragging) {
            var name = $(this).attr('name');
            var namee = $(this).attr('namee');
            // 把info标题的颜色改为结点所属类别的颜色
             $('#info h1').css('color', "black").text(namee);
            $('#info h5').css('color', "black").text(name);
            // 去掉旧的<p></p>
            $('#info p').remove();

            
	    // 增加各个人物的头像
            if (typeof(info[name]) != "undefined") {
                //avatar_ID = info[name]['ID'][0]
                //if(outlier_avatar_ID.indexOf(avatar_ID) != -1) {
                //    avatar_ID = avatar_ID + '0'
                //}
	    if ('主料' in info[name]){
		    $('#info').append('<p>' + '<img src="https://raw.githubusercontent.com/ngl567/CookBook-KG/master/visualization/recipe_photo/' + name + '.jpg" />' + '</p>');
	    }
            }
            for (var key in info[name]) {
                value = info[name][key];

                var flag_none = false;
                for (var item in value) {
                    if (value[item] == null || value[item] == 'N/A' || value[item] == '') {
                        flag_none = true;
                        break;
                    }
                } 
                if (flag_none == true) {              // 排除为空的属性值
                    continue;
                }

                $('#info').append('<p><span>' + key + '</span></p>');
		var item_info = '';
		count = 0
		for (var food_item in info[name][key]){
			if (count == 0){
				item_info = item_info + info[name][key][food_item];
			}
			else{
				item_info = item_info + "&nbsp;||&nbsp;" + info[name][key][food_item];
			}
			count = count + 1;
		}
		$('#info').append('<p>' + item_info + '</p>');
            }

            d3.select('#svg1 .nodes').selectAll('circle').attr('class', function(d){
                // 是目前悬浮的那个
                if (d.id == name) {
                    return '';
                }

                // 不是悬浮的那个，需要显示相邻的circle，对其他的圆圈做处理
                // 遍历图中的所有link
                for (var i = 0; i < graph.links.length; i++) {
                    if (graph.links[i]['source'].id == name && graph.links[i]['target'].id == d.id) {
                        return '';
                    }
                    if (graph.links[i]['target'].id == name && graph.links[i]['source'].id == d.id) {
                        return '';
                    }
                }

                return 'inactive';
            });

            // 处理连接line, 不相连的line不显示
            d3.select("#svg1 .links").selectAll('line').attr('class', function(d) {
                if (d.source.id == name || d.target.id == name) {
                    return '';
                } else {
                    return 'inactive';
                }
            });

            // 只显示之间相连的关系名
            d3.select("#svg1 .linetexts").selectAll('text').attr('class', function(d) {
                if (d.source.id == name || d.target.id == name) {
                    d3.select(this).attr('fill-opacity', 1);
                } else {
                    d3.select(this).attr('fill-opacity', 0);
                }
            })

            // UPDATE: 对于text也同时隐藏
            d3.select('#svg1 .texts').selectAll('text').attr('class', function(d){
                if (d.id == name) {
                    return '';
                }

                for (var i = 0; i < graph.links.length; i++) {
                    if (graph.links[i]['source'].id == name && graph.links[i]['target'].id == d.id) {
                        return '';
                    }
                    if (graph.links[i]['target'].id == name && graph.links[i]['source'].id == d.id) {
                        return '';
                    }
                }

                return 'inactive';
            });
        }
    });

    // 处理鼠标移开的事件上
    $('#svg1').on('mouseleave', '.nodes circle', function(event) {
        if (!dragging && 0) {
            
	    /*
            //如果搜索框还有东西，移开鼠标后仍然显示搜索的结果
            var name = $('#search input').val();
            d3.select('#svg1 .nodes').selectAll('circle').attr('class', function(d) {
                if (d.id.toLowerCase().indexOf(name.toLowerCase()) >= 0) {
                    return '';
                } else {
                   return 'inactive';
                }
            });
            d3.select('#svg1 .texts').selectAll('text').attr('class', function(d) {
                if (d.id.toLowerCase().indexOf(name.toLowerCase()) >= 0) {
                    return '';
                } else {
                    return 'inactive';
                }
            });
            d3.select("#svg1 .links").selectAll('line').attr('class', function(d) {
                return 'inactive';
            });
	    //d3.select('#svg1 .links').selectAll('line').attr('class', '');;
	    d3.select("#svg1 .linetexts").selectAll('text').attr('fill-opacity', function(d) {
                return 0;
            });
	    */
        }
        else if (!dragging) {
            
            // 否则，离开时把nodes和links的inactive去掉
            //d3.select('#svg1 .texts').selectAll('text').attr('class', '');;
            //d3.select('#svg1 .nodes').selectAll('circle').attr('class', '');;
            //d3.select('#svg1 .links').selectAll('line').attr('class', '');;
            d3.select("#svg1 .linetexts").selectAll('text').attr('fill-opacity', 0);
	    d3.select('#svg1 .nodes').selectAll('circle').attr('class', function(d){
                // 当前选中类型实体显示
                
		if (d.group == 0 && 1) {
		    return '';
		}
		else if (d.group == 1 && 1){
		    return '';
		}
		else if (d.group == 2 && 1){
		    return '';
		}
		else{
		    return 'inactive'
		}
            });
            
	    d3.select("#svg1 .links").selectAll('line').attr('class', function(d) {
		    return '';
            });
	    d3.select('#svg1 .texts').selectAll('text').attr('class', function(d){
                // 当前选中类型实体显示
		if (d.group == 0 ) {
		    return '';
		}
		else if (d.group == 1 ){
		    return '';
		}
		else if (d.group == 2 ){
		    return '';
		}
		else{
		    return 'inactive'
		}
            });
        }
    });

    $('#svg1').on('mouseenter', '.texts text', function(event) {
        if (!dragging) {
            var name = $(this).attr('name');

            // 把info标题的颜色改为结点所属类别的颜色
            $('#info h4').css('color', $(this).attr('fill')).text(name);
            // 去掉旧的<p></p>
            $('#info p').remove();

            
	    // 增加各个人物的头像
            if (typeof(info[name]) != "undefined") {
                //avatar_ID = info[name]['ID'][0]
                //if(outlier_avatar_ID.indexOf(avatar_ID) != -1) {
                //    avatar_ID = avatar_ID + '0'
                //}

	    if ('主料' in info[name]){
                $('#info').append('<p>' + '<img src="https://raw.githubusercontent.com/ngl567/CookBook-KG/master/visualization/recipe_photo/' + name + '.jpg" />' + '</p>');
	    }

            }
	    

            for (var key in info[name]) {
                value = info[name][key];

                var flag_none = false;
                for (var item in value) {
                    if (value[item] == null || value[item] == 'N/A' || value[item] == '') {
                        flag_none = true;
                        break;
                    }
                } 
                if (flag_none == true) {              // 排除为空的属性值
                    continue;
                }

		$('#info').append('<p><span>' + key + '</span></p>');
		var item_info = '';
		count = 0
		for (var food_item in info[name][key]){
			if (count == 0){
				item_info = item_info + info[name][key][food_item];
			}
			else{
				item_info = item_info + "&nbsp;||&nbsp;" + info[name][key][food_item];
			}
			count = count + 1;
		}
		$('#info').append('<p>' + item_info + '</p>');
                //$('#info').append('<p><span>' + key + '</span>' + info[name][key] + '</p>');
            }

            d3.select('#svg1 .texts').selectAll('text').attr('class', function(d){
                if (d.id == name) {
                    return '';
                }

                for (var i = 0; i < graph.links.length; i++) {
                    if (graph.links[i]['source'].id == name && graph.links[i]['target'].id == d.id) {
                        return '';
                    }
                    if (graph.links[i]['target'].id == name && graph.links[i]['source'].id == d.id) {
                        return '';
                    }
                }

                return 'inactive';
            });

            d3.select("#svg1 .links").selectAll('line').attr('class', function(d) {
                if (d.source.id == name || d.target.id == name) {
                    return '';
                } else {
                    return 'inactive';
                }
            });

            // 只显示之间相连的关系名
            d3.select("#svg1 .linetexts").selectAll('text').attr('class', function(d) {
                if (d.source.id == name || d.target.id == name) {
                    d3.select(this).attr('fill-opacity', 1);
                } else {
                    d3.select(this).attr('fill-opacity', 0);
                }
            })

            // UPDATE: 对于circle也同时隐藏
            d3.select('#svg1 .nodes').selectAll('circle').attr('class', function(d){
                // 是目前悬浮的那个
                if (d.id == name) {
                    return '';
                }

                // 不是悬浮的那个，需要显示相邻的circle，对其他的圆圈做处理
                // 遍历图中的所有link
                for (var i = 0; i < graph.links.length; i++) {
                    if (graph.links[i]['source'].id == name && graph.links[i]['target'].id == d.id) {
                        return '';
                    }
                    if (graph.links[i]['target'].id == name && graph.links[i]['source'].id == d.id) {
                        return '';
                    }
                }

                return 'inactive';
            });
        }
    });

    $('#svg1').on('mouseleave', '.texts text', function(event) {
        if (!dragging && 0) {
            
	    /*
            // 如果搜索框还有东西，移开鼠标后仍然显示搜索的结果
            var name = $('#search input').val();
            d3.select('#svg1 .nodes').selectAll('circle').attr('class', function(d) {
                if (d.id.toLowerCase().indexOf(name.toLowerCase()) >= 0) {
                   return '';
                } else {
                   return 'inactive';
                }
            });
            d3.select('#svg1 .texts').selectAll('text').attr('class', function(d) {
                if (d.id.toLowerCase().indexOf(name.toLowerCase()) >= 0) {
                    return '';
                } else {
                    return 'inactive';
                }
            });
            d3.select("#svg1 .links").selectAll('line').attr('class', function(d) {
                return 'inactive';
            });
	    //d3.select('#svg1 .links').selectAll('line').attr('class', '');;
	    d3.select("#svg1 .linetexts").selectAll('text').attr('fill-opacity', function(d) {
                return 0;
            });
	    */
        }
        else if (!dragging && 1) {
            
            // 否则，离开时把nodes和links的inactive去掉
            //d3.select('#svg1 .texts').selectAll('text').attr('class', '');;
            //d3.select('#svg1 .nodes').selectAll('circle').attr('class', '');;
            //d3.select('#svg1 .links').selectAll('line').attr('class', '');;
            d3.select("#svg1 .linetexts").selectAll('text').attr('fill-opacity', 0);
	    d3.select('#svg1 .nodes').selectAll('circle').attr('class', function(d){
                // 当前选中类型实体显示
		if (d.group == 0 && 1) {
		    return '';
		}
		else if (d.group == 1 && 1){
		    return '';
		}
		else if (d.group == 2 && 1){
		    return '';
		}
		else{
		    return 'inactive'
		}
            });
	    d3.select("#svg1 .links").selectAll('line').attr('class', function(d) {
		    return '';

            });
	    d3.select('#svg1 .texts').selectAll('text').attr('class', function(d){
                // 当前选中类型实体显示
		if (d.group == 0 && 1) {
		    return '';
		}
		else if (d.group == 1 && 1){
		    return '';
		}
		else if (d.group == 2 && 1){
		    return '';
		}
		else{
		    return 'inactive'
		}
            });
        }
    });

    // 结点信息框
    var info;

    d3.json("https://raw.githubusercontent.com/ngl567/CookBook-KG/master/visualization/entities_item_mimini.json", function(error, data){
        info = data;
        console.log(data)
    })
    
}
 );
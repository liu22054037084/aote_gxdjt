<!DOCTYPE html>
<html>
<head>
	<title>动漫后台管理系统</title>
	<!-- 引入Bootstrap样式 -->
	<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css">
	<!-- 引入jQuery和Bootstrap的JavaScript -->
	<script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
	<script src="https://cdn.bootcss.com/popper.js/1.12.9/umd/popper.min.js"></script>
	<script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
	<script type="text/javascript">
			const url = new URL(location.href);
			window.history.replaceState({}, document.title, url.origin);
	</script>
	<style>
		.resizeable {
			width: 1%;
			white-space: nowrap;
		}
		.btn-pink {
		  color: #fff;
		  background-color: #ff69b4;
		  border-color: #ff69b4;
		}
		
		.btn-pink:hover {
		  color: #fff;
		  background-color: #ff1493;
		  border-color: #ff1493;
		}
		.page-form {
		    display: flex;
		    justify-content: center;
		    align-items: center;
		}
		
		.input-group {
		    width: 128px; /* 根据需要调整宽度 */
		}
	</style>
</head>
<body>

<?php

// 连接到SQLite3数据库
try {
    $database = new SQLite3('/uup/admin/DS.db');
} catch (Exception $e) {
    die("无法连接数据库：" . $e->getMessage());
}

// 处理表单提交
if (isset($_POST['name']) && isset($_POST['like_l']) && isset($_POST['year']) && isset($_POST['quarter']) && isset($_POST['vod_state']) && isset($_POST['type_id']) && isset($_POST['vod_sub']) && isset($_POST['vod_pic']) && isset($_POST['vod_blurb'])) {
    $name = $_POST['name'];
    $like_l = $_POST['like_l'];
    $pattern = '/(?:\[|\(|\{|\s)(\d+)(?:\s*v\s*\d+)?(?:]|\)|}|\s)(\[\d*v\d]|\(\d*v\d\)|\[V\d]|\(V\d\))?.*/';
    $like_l = preg_replace($pattern, '', $like_l);
    $year = $_POST['year'];
    $quarter = $_POST['quarter'];
    $vod_state = $_POST['vod_state'];
    $type_id = $_POST['type_id'];
    $vod_sub = $_POST['vod_sub'];
    $vod_pic = $_POST['vod_pic'];
    $vod_time_add = time(); //获取时间戳
    $vod_blurb = $_POST['vod_blurb'];

    $params = array(
        ':name' => $name,
        ':like_l' => $like_l,
        ':year' => $year,
        ':quarter' => $quarter,
        ':vod_state' => $vod_state,
        ':type_id' => $type_id,
        ':vod_sub' => $vod_sub,
        ':vod_pic' => $vod_pic,
        ':vod_time_add' => $vod_time_add,
        ':vod_blurb' => $vod_blurb
    );

    $sql = "INSERT OR REPLACE INTO reserve_table (name, like_l, year, quarter, vod_state, type_id, vod_sub, vod_pic, vod_time_add, vod_blurb) 
            VALUES (:name, :like_l, :year, :quarter, :vod_state, :type_id, :vod_sub, :vod_pic, :vod_time_add, :vod_blurb)";

    // 使用预处理语句
    executeStatement($database, $sql, $params);
}

function executeStatement($database, $sql, $params)
{
    $stmt = $database->prepare($sql);
    foreach ($params as $param => &$value) {
        $stmt->bindParam($param, $value);
    }
    $stmt->execute();
}
?>
<div class="container">
    <h1 style="text-align: center;">动漫数据库信息录入</h1>
    <form method="POST">
        <div class="form-group">
            <label for="name">动漫名称:</label>
            <div style="display: flex; flex-direction: row; align-items: center;">
                <input type="text" class="form-control" id="name" name="name" placeholder="请输入动漫名称" style="flex-grow: 1;" required>
                <button type="button" id="wikiBtn" class="btn btn-primary" style="margin-left: 10px;background-color: #ffcf00;border-color: #ffe200;">维基搜索</button>
            </div>
        </div>
        <div class="form-group">
            <label for="vod_sub">动漫别名:</label>
            <input type="text" class="form-control" id="vod_sub" name="vod_sub" placeholder="注意别名为条件字段需要根据bt下载名称为条件！" required>
            <small class="form-text text-muted">例如: 动漫的英文或者罗马文</small>
        </div>
        <script>
            document.getElementById("wikiBtn").addEventListener("click", function() {
                var animeName = document.getElementById("name").value;
                var wikiUrl = "https://wiki.gxdjt.cf/w/index.php?search=" + encodeURI(animeName);
                window.open(wikiUrl, "_blank");
            });
        </script>
        <div class="form-group">
            <label for="like_l">模糊查询:</label>
            <input type="text" class="form-control" id="like_l" name="like_l" placeholder="请输入查询关键字" required>
            <small class="form-text text-muted">例如: 疾风</small>
        </div>
        <div class="form-group">
            <label for="vod_state">视频类型:</label>
            <select class="form-control" id="vod_state" name="vod_state" required>
				<option>请选择类型</option>
                <option value="TV">TV</option>
                <option value="OVA">OVA</option>
                <option value="剧场版">剧场版</option>
                <option value="抢先版">抢先版</option>
            </select>
            <small class="form-text text-muted">例如: 一月番剧</small>
        </div>
        <div class="form-group">
            <label for="year">发行年份:</label>
            <select class="form-control" id="year" name="year" required>
                <option>请选择年份</option>
                <?php
                $currentYear = date('Y');
                for ($year = $currentYear; $year >= 1950; $year--) {
                    echo "<option value='$year'>$year</option>";
                }
                ?>
            </select>
            <small class="form-text text-muted">例如: 2002</small>
        </div>
        <div class="form-group">
            <label for="quarter">发行月份:</label>
            <select class="form-control" id="quarter" name="quarter" required>
				<option>请选择发行月份</option>
                <option value="1">一月番剧</option>
                <option value="4">四月番剧</option>
                <option value="7">七月番剧</option>
                <option value="10">十月番剧</option>
            </select>
            <small class="form-text text-muted">例如: 一月番剧</small>
        </div>
        <div class="form-group">
            <label for="type_id">视频分类:</label>
            <select class="form-control" id="type_id" name="type_id" required>
				<option>请选择分类</option>
                <optgroup label="非新番">
                    <option value="1">国漫</option>
                    <option value="2">日韩</option>
                    <option value="3">欧美</option>
                </optgroup>
                <optgroup label="新番">
                    <option value="4">国漫</option>
                    <option value="5">日韩</option>
                    <option value="6">欧美</option>
                </optgroup>
            </select>
            <small class="form-text text-muted">例如: 新番</small>
        </div>
        <div class="form-group">
            <label for="vod_pic">宣传图片链接:</label>
            <input type="url" class="form-control" id="vod_pic" name="vod_pic" placeholder="为宣传图片链接，可以去维基百科寻得" required>
            <small class="form-text text-muted">例如:某图片链接 </small>
        </div>
        <script>
            var inputElement = document.getElementById("vod_pic");
            inputElement.addEventListener("change", function() {
                var inputValue = inputElement.value;
                if (inputValue.startsWith("https://upload.wikimedia.org")) {
                    inputValue = inputValue.replace("upload.wikimedia.org", "upload.gxdjt.cf");
                    inputElement.value = inputValue;
                }
            });
        </script>
        <div class="form-group">
            <label for="vod_blurb">动漫简介介绍:</label>
            <input type="text" class="form-control" id="vod_blurb" name="vod_blurb" placeholder="动漫简介介绍，可以去维基百科寻得" required>
            <small class="form-text text-muted">例如:xxxx,xxxx…… </small>
        </div>
        <button type="submit" class="btn btn-primary">添加数据</button>
        <button type="button" class="btn btn-pink" data-toggle="modal" data-target="#xiugaishuju">修改数据</button>
        <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#deleteModal">删除数据</button>
        <button type="button" class="btn btn-info" data-toggle="modal" data-target="#searchModal">搜索数据</button>
    </form>
	<hr>

	<!-- 显示数据表格 -->
	<?php
        // 设置每页记录数和默认页码
        $records_per_page = 5;
        $page_number = isset($_GET['page']) ? $_GET['page'] : 1;
        
        if (isset($_POST['name_q'])) {
          // 处理搜索表单的提交
          $name = $_POST['name_q'];
        
          // 获取所有记录数
          $total_records = $database->querySingle("SELECT COUNT(*) FROM reserve_table WHERE name = '{$name}' OR name LIKE '%{$name}%'");
        
          // 计算总页数
          $total_pages = ceil($total_records / $records_per_page);
        
          // 计算偏移量和限制记录数
          $offset = ($page_number - 1) * $records_per_page;
          $limit = $records_per_page;
        
          // 执行查询获取数据
          $query = "SELECT * FROM reserve_table WHERE name LIKE ? LIMIT ? OFFSET ?";
          $stmt = $database->prepare($query);
          $stmt->bindValue(1, '%' . $name . '%', SQLITE3_TEXT);
          $stmt->bindValue(2, $limit, SQLITE3_INTEGER);
          $stmt->bindValue(3, $offset, SQLITE3_INTEGER);
          $result = $stmt->execute();
        
          // 显示数据表格
          $num_rows = 0;
          while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $num_rows++;
            if ($num_rows == 1) {
              echo "<div class='table-responsive'>";
              echo "<h2>搜索结果:</h2>";
              echo "<table class='table table-striped table-bordered'>";
              echo "<thead>";
              echo "<tr>";
              echo "<th class='resizeable'>动漫名称</th>"; //name
			  echo "<th class='resizeable'>模糊字段</th>"; //like_l
			  echo "<th class='resizeable'>宣传图片</th>"; //vod_pic
			  echo "<th class='resizeable'>发行年份</th>"; //year
			  echo "<th class='resizeable'>发行季度</th>"; //quarter
			  echo "<th class='resizeable'>动漫别名</th>"; //vod_sub
			  echo "<th class='resizeable'>动漫拼音</th>"; //vod_en
			  echo "<th class='resizeable'>动漫首字</th>"; //vod_letter
			  echo "<th class='resizeable'>视频类型</th>"; //vod_state
              echo "<th class='resizeable'>类型地区</th>"; //type_id
              echo "<th class='resizeable'>现时间戳</th>"; //vod_time_add
              echo "<th class='resizeable'>动漫简介</th>"; //vod_blurb
              echo "</tr>";
              echo "</thead>";
              echo "<tbody>";
            }
        
            echo "<tr>";
            echo "<td class='resizeable'>".$row['name']."</td>";
            echo "<td class='resizeable'>".$row['like_l']."</td>";
			echo "<td class='resizeable'><img src='".$row['vod_pic']."' style='width:100%;' /></td>";
			echo "<td class='resizeable'>".$row['year']."</td>";
			echo "<td class='resizeable'>".$row['quarter']."</td>";
			echo "<td class='resizeable'>".$row['vod_sub']."</td>";
			echo "<td class='resizeable'>".$row['vod_en']."</td>";
			echo "<td class='resizeable'>".$row['vod_letter']."</td>";
			echo "<td class='resizeable'>".$row['vod_state']."</td>";
            echo "<td class='resizeable'>".$row['type_id']."</td>";
            echo "<td class='resizeable'>".$row['vod_time_add']."</td>";
            echo "<td class='resizeable'>".$row['vod_blurb']."</td>";
            echo "</tr>";
          }
        
          if ($num_rows == 0) {
            echo "<p id='su-sg' class='alert alert-info'>没有找到匹配的数据</p>";
			echo "<script>
			  setTimeout(function() {
			    var errorMsg = document.getElementById('su-sg');
			    errorMsg.parentNode.removeChild(errorMsg);
			  }, 2000);
			</script>";
          } else {
            echo "</tbody>";
            echo "</table>";
            echo "</div>";
          }
        }
		echo "<nav>";
		echo "<ul class='pagination justify-content-center'>";
		for ($i = 1; $i <= $total_pages; $i++) {
		  echo "<li class='page-item ".($i == $page_number ? 'active' : '')."'>";
		  echo "<a class='page-link' href='?page={$i}&name_q={$name}'>{$i}</a>";
		  echo "</li>";
		}
		echo "</ul>";
		echo "</nav>";
    ?>
	<h2>数据列表</h2>
    <?php
        // 获取总记录数
        $query = "SELECT COUNT(*) AS count FROM reserve_table";
        $result = $database->querySingle($query);
        $total_records = intval($result);
        
        $limit = 5; // 每页显示的记录数
        $total_pages = ceil($total_records / $limit);
        
        // 获取当前页码，默认为最后一页
        $page = isset($_GET['page']) ? intval($_GET['page']) : $total_pages;
        
        // 校正页码，确保在有效范围内
        $page = max(1, min($total_pages, $page));
        
        // 计算偏移量
        $offset = ($page - 1) * $limit;
        
        // 查询当前页的数据
        $query = "SELECT * FROM reserve_table LIMIT $limit OFFSET $offset";
        $result = $database->query($query);
    ?> 
    <div class="table-responsive">
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th class="resizeable">动漫名称</th>
                    <th class="resizeable">模糊字段</th>
                    <th class="resizeable">宣传图片</th>
                    <th class="resizeable">发行年份</th>
                    <th class="resizeable">发行季度</th>
                    <th class="resizeable">动漫别名</th>
                    <th class="resizeable">动漫拼音</th>
                    <th class="resizeable">动漫首字</th>
                    <th class="resizeable">视频类型</th>
                    <th class="resizeable">类型地区</th>
                    <th class="resizeable">现时间戳</th>
                    <th class="resizeable">动漫简介</th>
                </tr>
            </thead>
            <tbody>
                <?php while ($row = $result->fetchArray(SQLITE3_ASSOC)) { ?>
                    <tr>
                        <td class="resizeable"><?php echo $row['name']; ?></td>
                        <td class="resizeable"><?php echo $row['like_l']; ?></td>
                        <td class="resizable"><img src="<?php echo $row['vod_pic']; ?>" style="width:100%;" /></td>
                        <td class="resizeable"><?php echo $row['year']; ?></td>
                        <td class="resizeable"><?php echo $row['quarter']; ?></td>
                        <td class="resizeable"><?php echo $row['vod_sub']; ?></td>
                        <td class="resizeable"><?php echo $row['vod_en']; ?></td>
                        <td class="resizeable"><?php echo $row['vod_letter']; ?></td>
                        <td class="resizeable"><?php echo $row['vod_state']; ?></td>
                        <td class="resizeable"><?php echo $row['type_id']; ?></td>
                        <td class="resizeable"><?php echo $row['vod_time_add']; ?></td>
                        <td class="resizeable"><?php echo $row['vod_blurb']; ?></td>
                    </tr>
                <?php } ?>
            </tbody>
        </table>
    </div>
    
    <?php
    // 计算总页数
    $query = "SELECT COUNT(*) AS count FROM reserve_table";
    $result = $database->querySingle($query);
    $total_pages = ceil($result / $limit);
    
    // 限制显示的按钮数为七个
    $max_visible_buttons = 5;
    
    // 计算起始页码和结束页码
    $start_page = max(1, $page - floor($max_visible_buttons / 2));
    $end_page = min($start_page + $max_visible_buttons - 1, $total_pages);
    
    // 调整起始页码
    $start_page = max(1, $end_page - $max_visible_buttons + 1);
    ?>
    
    <nav aria-label="分页导航">
        <ul class="pagination justify-content-center">
            <?php if ($page > 1) { ?>
                <li class="page-item">
                    <a class="page-link" href="?page=1" aria-label="首页">
                        <span aria-hidden="true">&laquo;</span>
                        <span class="sr-only">首页</span>
                    </a>
                </li>
            <?php } ?>
    
            <?php if ($start_page > 1) { ?>
                <li class="page-item">
                    <a class="page-link" href="?page=<?php echo $start_page - 1; ?>" aria-label="上一页">
                        <span aria-hidden="true">&lsaquo;</span>
                        <span class="sr-only">上一页</span>
                    </a>
                </li>
            <?php } ?>
    
            <?php for ($i = $start_page; $i <= $end_page; $i++) { ?>
                <li class="page-item <?php echo $page === $i ? 'active' : ''; ?>">
                    <a class="page-link" href="?page=<?php echo $i; ?>"><?php echo $i; ?></a>
                </li>
            <?php } ?>
    
            <?php if ($end_page < $total_pages) { ?>
                <li class="page-item">
                    <a class="page-link" href="?page=<?php echo $end_page + 1; ?>" aria-label="下一页">
                        <span aria-hidden="true">&rsaquo;</span>
                        <span class="sr-only">下一页</span>
                    </a>
                </li>
            <?php } ?>
    
            <?php if ($page < $total_pages) { ?>
                <li class="page-item">
                    <a class="page-link" href="?page=<?php echo $total_pages; ?>" aria-label="尾页">
                        <span aria-hidden="true">&raquo;</span>
                        <span class="sr-only">尾页</span>
                    </a>
                </li>
            <?php } ?>
    		
    		<li>
    			<form action="" method="GET" class="page-form">
    			    <div class="input-group">
    			        <select name="page" class="form-control" style="margin-left: 4px;">
    					<?php
    					    for ($i =  $total_pages; $i > 0; $i--) {
    					        echo "<option value='$i'>$i</option>";
    					    }
    					    ?>
    					</select>
    			        <div class="input-group-append">
    			            <button type="submit" class="btn btn-primary">跳转</button>
    			        </div>
    			    </div>
    			</form>
    		</li>
    	</ul>
    </nav>
    	
	<!-- 修改数据的模态框 -->
	<div class="modal fade" id="xiugaishuju" tabindex="-1" role="dialog" aria-labelledby="xiugaishujuLabel" aria-hidden="true">
	    <div class="modal-dialog" role="document">
	        <div class="modal-content">
	            <div class="modal-header">
	                <h5 class="modal-title" id="xiugaishujuLabel">修改数据</h5>
	                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
	                    <span aria-hidden="true">&times;</span>
	                </button>
	            </div>
	            <div class="modal-body">
	                <form method="POST">
	                    <div class="form-group">
	                        <label for="name_x">动漫名称:</label>
	                        <input type="text" class="form-control" id="name_x" name="name_x" placeholder="修改的动漫名称" required>
	                    </div>
						<div class="form-group">
						    <label for="vod_sub_x">动漫别名:</label>
						    <input type="text" class="form-control" id="vod_sub_x" name="vod_sub_x">
						</div>
						<div class="form-group">
						    <label for="like_l_x">模糊查询:</label>
						    <input type="text" class="form-control" id="like_l_x" name="like_l_x">
						</div>
						<div class="form-group">
						    <label for="vod_state_x">视频类型:</label>
						    <select class="form-control" id="vod_state_x" name="vod_state_x">
								<option value="">请选择类型</option>
						        <option value="TV">TV</option>
						        <option value="OVA">OVA</option>
						        <option value="剧场版">剧场版</option>
						        <option value="抢先版">抢先版</option>
						    </select>
						</div>
						<div class="form-group">
						    <label for="year_x">发行年份:</label>
						    <select class="form-control" id="year_x" name="year_x">
						        <option value="">请选择年份</option>
						        <?php
						        $currentYear = date('Y');
						        for ($year = $currentYear; $year >= 1950; $year--) {
						            echo "<option value='$year'>$year</option>";
						        }
						        ?>
						    </select>
						</div>
						<div class="form-group">
						    <label for="quarter_x">发行月份:</label>
						    <select class="form-control" id="quarter_x" name="quarter_x">
								<option value="">请选择发行月份</option>
						        <option value="1">一月番剧</option>
						        <option value="4">四月番剧</option>
						        <option value="7">七月番剧</option>
						        <option value="10">十月番剧</option>
						    </select>
						</div>
						<div class="form-group">
						    <label for="type_id_x">视频分类:</label>
						    <select class="form-control" id="type_id_x" name="type_id_x">
								<option value="">请选择分类</option>
						        <optgroup label="非新番">
						            <option value="1">国漫</option>
						            <option value="2">日韩</option>
						            <option value="3">欧美</option>
						        </optgroup>
						        <optgroup label="新番">
						            <option value="4">国漫</option>
						            <option value="5">日韩</option>
						            <option value="6">欧美</option>
						        </optgroup>
						    </select>
						</div>
						<div class="form-group">
						    <label for="vod_pic_x">宣传图片链接:</label>
						    <input type="url" class="form-control" id="vod_pic_x" name="vod_pic_x">
						</div>
						<script>
						    var inputElement = document.getElementById("vod_pic");
						    inputElement.addEventListener("change", function() {
						        var inputValue = inputElement.value;
						        if (inputValue.startsWith("https://upload.wikimedia.org")) {
						            inputValue = inputValue.replace("upload.wikimedia.org", "upload.gxdjt.cf");
						            inputElement.value = inputValue;
						        }
						    });
						</script>
						<div class="form-group">
						    <label for="vod_blurb_x">动漫简介介绍:</label>
						    <input type="text" class="form-control" id="vod_blurb_x" name="vod_blurb_x">
						</div>
	                    <button type="submit" class="btn btn-pink">修改数据</button>
	                </form>
	            </div>
	        </div>
	    </div>
	</div>
	
    <!-- 删除数据的模态框 -->
    <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="deleteModalLabel">删除数据</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form method="POST">
                        <div class="form-group">
                            <label for="name_d">动漫名称:</label>
                            <input type="text" class="form-control" id="name_d" name="name_d" placeholder="请输入动漫名称" required>
                            <small class="form-text text-muted">例如: Naruto</small>
                        </div>
                        <button type="submit" class="btn btn-danger">删除数据</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 搜索数据的模态框 -->
    <div class="modal fade" id="searchModal" tabindex="-1" role="dialog" aria-labelledby="searchModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="searchModalLabel">搜索数据</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form method="POST">
                        <div class="form-group">
                            <label for="name_q">动漫名称:</label>
                            <input type="text" class="form-control" id="name_q" name="name_q" placeholder="请输入动漫名称">
                            <small class="form-text text-muted">例如: Naruto</small>
                        </div>
                        <button type="submit" class="btn btn-info">搜索数据</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
<?php
	//处理修改数据的值
	if (isset($_POST['name_x'])) {
		$name = $_POST['name_x'];
		$list = [];

		if ($_POST['like_l_x'] != "") {
			$pattern = '/(?:\[|\(|\{|\s)(\d+)(?:\s*v\s*\d+)?(?:]|\)|}|\s)(\[\d*v\d]|\(\d*v\d\)|\[V\d]|\(V\d\))?.*/';
			$like_l_x = preg_replace($pattern, '', $_POST['like_l_x']);
		    $list[] = "like_l = '{$like_l_x}'";
		}
		
		if ($_POST['vod_sub_x'] != "") {
		    $list[] = "vod_sub = '{$_POST['vod_sub_x']}'";
		}
		
		if ($_POST['vod_state_x'] != "") {
		    $list[] = "vod_state = '{$_POST['vod_state_x']}'";
		}
		
		if ($_POST['year_x'] != "") {
		    $list[] = "year = '{$_POST['year_x']}'";
		}
		
		if ($_POST['quarter_x'] != "") {
		    $list[] = "quarter = '{$_POST['quarter_x']}'";
		}
		
		if ($_POST['type_id_x'] != "") {
		    $list[] = "type_id = '{$_POST['type_id_x']}'";
		}
		
		if ($_POST['vod_pic_x'] != "") {
		    $list[] = "vod_pic = '{$_POST['vod_pic_x']}'";
		}
		
		if ($_POST['vod_blurb_x'] != "") {
		    $list[] = "vod_blurb = '{$_POST['vod_blurb_x']}'";
		}

		$join_list = implode(', ', $list);

		$query = "UPDATE reserve_table SET $join_list WHERE name = '$name'";
		echo $query;
		$stmt = $database->prepare($query);
		$result = $stmt->execute();

		if ($result && $database->changes() > 0) {
			// 更新成功后重建索引
			$database->exec("REINDEX reserve_table");
			echo "<script>window.location.href = 'i.php?msg=更改成功';</script>";
		} else {
			echo "<p id='error-msg' class='alert alert-danger'>更新失败，请检查输入的名称是否正确</p>";
			echo "<script>
			  setTimeout(function() {
				var errorMsg = document.getElementById('error-msg');
				errorMsg.parentNode.removeChild(errorMsg);
			  }, 2000);
			</script>";
		}
	}

	// 处理删除数据的请求
	if (isset($_POST['name_d'])) {
		$name = $_POST['name_d'];
		$query = "DELETE FROM reserve_table WHERE name=?";
		$stmt = $database->prepare($query);
		$stmt->bindValue(1, $name, SQLITE3_TEXT);
		$result = $stmt->execute();
		if ($result && $database->changes() > 0) {
			// 删除成功后重建索引
			$database->exec("REINDEX reserve_table");
			echo "<script>window.location.href = 'i.php?msg=删除成功';</script>";
		} else{
			echo "<p id='error-msg' class='alert alert-danger'>删除失败，请检查输入的名称是否正确</p>";
			echo "<script>
			  setTimeout(function() {
			    var errorMsg = document.getElementById('error-msg');
			    errorMsg.parentNode.removeChild(errorMsg);
			  }, 2000);
			</script>";
		}
	}
	if (isset($_GET['msg'])) {
	    $msg = $_GET['msg'];
	    echo "<p id='success-msg' class='alert alert-success'>$msg</p>";
	    // 添加 JavaScript，将消息隐藏或删除
	    echo "<script>
	        // 设置定时器，将消息隐藏或删除
	        setTimeout(function() {
	            var successMsg = document.getElementById('success-msg');
				successMsg.style.display = 'none';
	        }, 2000); // 消息显示 2 秒钟
	    </script>";
	    exit();
	}
?>
</body>
</html>
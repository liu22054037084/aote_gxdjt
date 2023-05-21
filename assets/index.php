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
	</style>
</head>
<body>

<?php


// type_id(类型的id)
// vod_sub(影视别名)
// vod_pic(图)
// vod_time_add(添加时间戳)
// vod_blurb(简介)


    // 连接到SQLite3数据库
    try {
        $database = new SQLite3('./DS.db');
    } catch (Exception $e) {
        die("无法连接数据库：" . $e->getMessage());
    }
    
    // 处理表单提交
    if (isset($_POST['name'])) {
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
		
    
    	// 使用预处理语句
    	$stmt = $database->prepare("INSERT OR REPLACE INTO reserve_table (name, like_l, year, quarter, vod_state, type_id, vod_sub, vod_pic, vod_time_add, vod_blurb) VALUES (:name, :like_l, :year, :quarter, :vod_state, :type_id, :vod_sub, :vod_pic, :vod_time_add, :vod_blurb)");
    		$stmt->bindParam(':name', $name);
    		$stmt->bindParam(':like_l', $like_l);
    		$stmt->bindParam(':year', $year);
    		$stmt->bindParam(':quarter', $quarter);
			$stmt->bindParam(':vod_state', $vod_state);
    		$stmt->bindParam(':type_id', $type_id); // type_id(类型的id)
    		$stmt->bindParam(':vod_sub', $vod_sub); // vod_sub(影视别名)
    		$stmt->bindParam(':vod_pic', $vod_pic); // vod_pic(图)
    		$stmt->bindParam(':vod_time_add', $vod_time_add); // vod_time_add(添加时间戳)
    		$stmt->bindParam(':vod_blurb', $vod_blurb); // vod_blurb(简介)
    		$stmt->execute();
    	}
?>


<div class="container">
	<h1 style="text-align: center;">动漫数据库信息录入</h1>
	<form method="POST">
	    <div class="form-group">
	        <label for="name">动漫名称:</label>
			<div style="display: flex; flex-direction: row; align-items: center;">
	        <input type="text" class="form-control" id="name" name="name" placeholder="请输入动漫名称" required style="flex-grow: 1;">
	        <button type="button" id="wikiBtn" class="btn btn-primary" style="margin-left: 10px;background-color: #ffcf00;border-color: #ffe200;">维基搜索</button>
			</div>
	    </div>
		<div class="form-group">
		    <label for="vod_sub">动漫别名:</label>
		    <input type="text" class="form-control" id="vod_sub" name="vod_sub" placeholder="注意别名为条件字段需要根据rss下载名称为条件！" required>
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
	            <option value="">请选择年份</option>
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
	    <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#deleteModal">删除数据</button>
	    <button type="button" class="btn btn-info" data-toggle="modal" data-target="#searchModal">搜索数据</button>
	</form>

	<hr>

	<!-- 显示数据表格 -->
	<?php
        // 设置每页记录数和默认页码
        $records_per_page = 10;
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
			  echo "<th class='resizeable'>动漫别名</th>"; //vod_sub
			  echo "<th class='resizeable'>动漫拼音</th>"; //vod_en
			  echo "<th class='resizeable'>动漫首字</th>"; //vod_letter
			  echo "<th class='resizeable'>视频类型</th>"; //vod_state
              echo "<th class='resizeable'>模糊字段</th>"; //like_l
              echo "<th class='resizeable'>发行年份</th>"; //year
			  echo "<th class='resizeable'>发行季度</th>"; //quarter
              echo "<th class='resizeable'>类型地区</th>"; //type_id
			  echo "<th class='resizeable'>宣传图片</th>"; //vod_pic
              echo "<th class='resizeable'>现时间戳</th>"; //vod_time_add
              echo "<th class='resizeable'>动漫简介</th>"; //vod_blurb
              echo "</tr>";
              echo "</thead>";
              echo "<tbody>";
            }
        
            echo "<tr>";
            echo "<td class='resizeable'>".$row['name']."</td>";
            echo "<td class='resizeable'>".$row['vod_sub']."</td>";
			echo "<td class='resizeable'>".$row['vod_en']."</td>";
			echo "<td class='resizeable'>".$row['vod_letter']."</td>";
			echo "<td class='resizeable'>".$row['vod_state']."</td>";
            echo "<td class='resizeable'>".$row['like_l']."</td>";
            echo "<td class='resizeable'>".$row['year']."</td>";
            echo "<td class='resizeable'>".$row['quarter']."</td>";
            echo "<td class='resizeable'>".$row['type_id']."</td>";
			echo "<td class='resizeable'><img src='".$row['vod_pic']."' style='width:100%;' /></td>";
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
        // 获取当前页码
        $page = isset($_GET['page']) ? intval($_GET['page']) : 1;
        $limit = 10; // 每页显示的记录数
        $offset = ($page - 1) * $limit;
    
        // 查询表格中的所有数据
        $query = "SELECT * FROM reserve_table LIMIT $limit OFFSET $offset";
        $result = $database->query($query);
    ?>
    <div class="table-responsive">
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                  <th class="resizeable">动漫名称</th>
                  <th class="resizeable">动漫别名</th>
				  <th class="resizeable">动漫拼音</th>
				  <th class="resizeable">动漫首字</th>
				  <th class="resizeable">视频类型</th>
                  <th class="resizeable">模糊字段</th>
                  <th class="resizeable">发行年份</th>
                  <th class="resizeable">发行季度</th>
                  <th class="resizeable">类型地区</th>
				  <th class="resizeable">宣传图片</th>
                  <th class="resizeable">现时间戳</th>
                  <th class="resizeable">动漫简介</th>
                </tr>
            </thead>
            <tbody>
                <?php while ($row = $result->fetchArray(SQLITE3_ASSOC)) { ?>
                <tr>
                    <td class="resizeable"><?php echo $row['name']; ?></td>
                    <td class="resizeable"><?php echo $row['vod_sub']; ?></td>
					<td class="resizeable"><?php echo $row['vod_en']; ?></td>
					<td class="resizeable"><?php echo $row['vod_letter']; ?></td>
					<td class="resizeable"><?php echo $row['vod_state']; ?></td>
                    <td class="resizeable"><?php echo $row['like_l']; ?></td>
                    <td class="resizeable"><?php echo $row['year']; ?></td>
                    <td class="resizeable"><?php echo $row['quarter']; ?></td>
                    <td class="resizeable"><?php echo $row['type_id']; ?></td>
					<td class="resizable"><img src="<?php echo $row['vod_pic']; ?>" style="width:100%;" /></td>
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
    ?>
    
    <nav aria-label="分页导航">
        <ul class="pagination justify-content-center">
            <?php for ($i = 1; $i <= $total_pages; $i++) { ?>
            <li class="page-item <?php echo $page === $i ? 'active' : ''; ?>">
                <a class="page-link" href="?page=<?php echo $i; ?>"><?php echo $i; ?></a>
            </li>
            <?php } ?>
        </ul>
    </nav>
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
			echo "<script>window.location.href = 'i.php';</script>";
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
<?php
/**
 * config.php 系统配置：数据库连接、显示信息等
 * ----------------------------------------------------------------
 * OldCMS,site:http://www.oldcms.com
 */

/* 数据库连接 */
$config['dbHost']		= "";			//数据库地址
$config['dbUser']		= "";				//用户
$config['dbPwd']		= "";				//密码
$config['database']		= "";			//数据库名
$config['charset']		='utf8';				//数据库字符集
$config['tbPrefix']		='oc_';					//表名前缀
$config['dbType']		='mysql';				//数据库类型(目前只支持mysql)

/* 注册配置 */
$config['register']		='normal';				//normal,正常;invite,只允许邀请注册;close,关闭注册功能
$config['mailauth']		=false;					//注册时是否邮箱验证

/* url配置 */
$config['urlroot']		='http://xsserme.sinaapp.com';//访问的url起始
$config['urlrewrite']	=false;					//是否启用Url Rewrite

/* 存储配置 */
$config['filepath']		=ROOT_PATH.'/upload';	//文件存储目录,结尾无'/'
$config['fileprefix']	=$config['urlroot'].'/upload'; //访问文件起始,结尾无'/'

/* 主题选择 */
$config['theme']		='default';				//主题选择
$config['template']		='default';				//模板选择

/* 显示设置 */
$config['show']=array(
	'sitename'			=>'齐迹的xss平台',											//网站名
	'sitedesc'			=>'齐迹的xss平台',								//一句话简介
	'keywords'			=>'齐迹的xss平台',			//keywords
	'description'		=>'齐迹的xss平台',	//description
	'adminmail'			=>'xsserme@sina.cn'
);

/* 积分等级设置 */
$config['point']=array(
	'award'=>array(
		'publish'		=>2,
		'comment'		=>2,
		'invitereg'		=>10 					//邀请注册奖励
	)
);

/* 其它设置 */
$config['timezone']		='Asia/Shanghai';		//时区，如UTC
$config['expires']		=3600;					//过期时长(秒)
$config['debug']		=false;					//调试模式(是否显示程序、数据库等错误)
//邮箱配置
$config['email']		="";
$config['emailpwd']		="";
?>
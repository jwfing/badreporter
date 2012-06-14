CREATE TABLE IF NOT EXISTS av_badcases(
    id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
    url varchar(1024) NOT NULL,
    description varchar(2048) DEFAULT NULL,
    status varchar(1) DEFAULT 'A',
    createTime DateTime,
    updateTime DateTime,
    PRIMARY KEY (id),
    KEY url_idx (url)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

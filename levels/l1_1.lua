return function(level)
    local psz = level:Point2(100,20)
    level:Platform(level:Point2(15,150),level:Point2(100,20))
    level:Platform(level:Point2(100,500),psz)
    level:Platform(level:Point2(200,450),psz)
end
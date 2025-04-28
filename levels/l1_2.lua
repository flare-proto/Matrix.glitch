return function(level)
    local psz = level:Point2(100,20)
    level:Platform(level:Point2(470,100),level:Point2(100,20))
    level:Platform(level:Point2(100,600),psz)
    level:Platform(level:Point2(200,400),psz)
    level:exit(level:Point2(500,300))
    level:player(level:Point2(100, 400))
end
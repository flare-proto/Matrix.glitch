return function(level)
    local psz = level:Point2(100,20)
    level:Platform(level:Point2(15,150),level:Point2(100,20))
    level:Platform(level:Point2(100,600),psz)
    level:Platform(level:Point2(200,550),psz)
    level:exit(level:Point2(500,300))
end
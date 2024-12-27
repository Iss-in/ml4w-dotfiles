
-- default = "Media"

-- node_monitor.add_listener("node-appeared", function(node)
--   -- Check for specific media roles
--   local mediaRole = node.properties["media.role"]

--   if mediaRole == "notification" or mediaRole == "phone-call" then
--     -- Set ducking priority for these roles
--     node.properties["media.role"] = mediaRole
--     node.properties["media.ducking-priority"] = 1
--   end
-- end)

-- -- Handle the "ducking" effect
-- node_monitor.add_listener("node-state-changed", function(node, oldState, newState)
--   if node.properties["media.ducking-priority"] == 1 and newState == "playing" then
--     -- Apply ducking to other sounds
--     for _, sinkNode in ipairs(node_monitor.list_sinks()) do
--       if sinkNode.properties["media.role"] == "Media" then
--         sinkNode.volume = sinkNode.volume * 0.5 -- Lower the volume by 50%
--       end
--     end
--   end
-- end)
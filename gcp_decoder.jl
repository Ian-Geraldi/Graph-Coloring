function gcp_decode1!(chromosome:: Array{Float64}, instance:: gcpInstance, rewrite::Bool):: Int64
    instance = gcpInstance(instance)
    node_order = sortperm(chromosome)
    uncolored_nodes = instance.num_vertices
    i = 1
    while uncolored_nodes>0 && i<=instance.num_vertices
        current_node_id = node_order[i]
        if !isnothing(instance.nodes[current_node_id].color)
            throw(ArgumentError("Trying to paint already painted node"))
            i += 1
            continue
        end
        needs_new_color = true
        for c in 1:instance.num_colors
            if can_paint(node_order[i], instance, c)
                paint(current_node_id, instance, c)
                uncolored_nodes -= 1
                needs_new_color = false
                i+=1
                break
            end
        end
        if needs_new_color
            instance.num_colors += 1
            paint(current_node_id, instance, instance.num_colors)
            uncolored_nodes -= 1
            i+=1
        end
    end
    return instance.num_colors
end
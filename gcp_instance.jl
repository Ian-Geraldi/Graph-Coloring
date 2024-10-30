################################################################################
# graph_instance.jl: data structures and support function to deal with instances
# of graphs in DIMACS format.
#
# Created on: Oct 29, 2024
#
################################################################################

"""
    struct gcpInstance
Represents a graph instance in DIMACS format. The constructor loads a graph from
a file containing lines in the following format:
    c Comment lines (optional)
    p edge num_vertices num_edges
    e vertex1 vertex2
    ...
For example:
    c This is a comment
    p edge 3 2
    e 1 2
    e 2 3

**NOTE** that this structure inherits from `AbstractInstance` conforming
required signatures.
"""

mutable struct Node
    id::Int64
    color::Union{Int64, Nothing}
    neighbors::Vector{Int64}

    function Node(id::Int64)
        new(id, nothing, Int64[])
    end
end

mutable struct gcpInstance <: AbstractInstance
    num_vertices::Int64
    num_edges::Int64
    num_colors::Int64
    nodes::Vector{Node}

    function gcpInstance(filename::String)
        # Initialize with empty values
        num_vertices = 0
        num_edges = 0
        num_colors = 1
        nodes = Node[]
        
        
        if !isfile(filename)
            throw(ArgumentError("File not found: $filename"))
        end

        lines = Array{String,1}()
        try
            open(filename) do file
                lines = readlines(file)
            end
        catch err
            throw(LoadError(filename, 0, "cannot read '$filename'"))
        end

        if length(lines) == 0
            throw(LoadError(filename, 0, "file is empty"))
        end

        # Process the file
        found_problem_line = false
        line_number = 0

        try
            for (i, line) in enumerate(lines)
                line_number = i
                if isempty(line)
                    continue
                end

                type = line[1]
                if type == 'c'
                    continue
                elseif type == 'p'
                    # Problem line
                    parts = split(line)
                    if length(parts) != 4 || parts[2] != "edge"
                        throw(ArgumentError("Invalid problem line format"))
                    end
                    
                    num_vertices = parse(Int64, parts[3])
                    num_edges = parse(Int64, parts[4])
                    nodes = Vector{Node}(undef, num_vertices)
                    for i in 1:num_vertices
                        nodes[i] = Node(i)
                    end
                    found_problem_line = true
                
                elseif type == 'e'
                    if !found_problem_line
                        throw(ArgumentError("Edge line before problem line"))
                    end
                    
                    # Edge line
                    parts = split(line)
                    if length(parts) != 3
                        throw(ArgumentError("Invalid edge line format"))
                    end
                    
                    v1_id = parse(Int64, parts[2])
                    v2_id = parse(Int64, parts[3])
                    push!(nodes[v1_id].neighbors, v2_id)
                    push!(nodes[v2_id].neighbors, v1_id)
                end
            end

        catch err
            if isa(err, ArgumentError)
                throw(LoadError(filename, line_number, 
                    "error line $(line_number) of '$filename': $(err.msg)"))
            else
                throw(LoadError(filename, line_number,
                    "error line $(line_number) of '$filename'"))
            end
        end

        if !found_problem_line
            throw(LoadError(filename, 0, "no problem line found in file"))
        end

        new(num_vertices, num_edges, num_colors, nodes)
    end
    
    function gcpInstance(instance:: gcpInstance)
        new(instance.num_vertices, instance.num_edges, instance.num_colors, deepcopy(instance.nodes))
    end
end

function can_paint(node_id::Int64, instance::gcpInstance, color::Int64)
    for neighbor in instance.nodes[node_id].neighbors
        if instance.nodes[neighbor].color == color
            return false
        end
    end
    return true
end

function paint(node_id::Int64, instance::gcpInstance, color::Int64)
    instance.nodes[node_id].color = color
end

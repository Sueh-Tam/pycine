@extends('layouts.app')

@section('title', $task->title)

@section('content')
<div class="mb-4">
    <a href="{{Route('tasks.index')}}"
        class="link">
        <- Go back to the task list
    </a>
</div>
<p class="mb-4 text-slate-700">{{$task->description}}</p>

@if ($task->long_description)
    <p>{{$task->long_description}}</p>
@endif

<p class="mb-4 text-sm text-slate-500">Created {{$task->created_at->diffForHumans()}} * Updated{{$task->updated_at->diffForHumans()}}</p>


<p class="mb-4">
    @if ($task->completed)
        <span class="font-medium text-green-500">
            Completed
        </span>
    @else 
        <span class="font-medium text-red-500">
            Not completed
        </span>
    @endif
</p>

<div class="flex gap-2">
    <form action="{{Route('tasks.toggle-complete',['task' => $task])}}" method="POST">
        @method('put')
        @csrf
        <button type="submit" class="btn">
            Mark as {{$task->completed ? 'Not completed': 'completed'}}
        </button>
    </form>
    <a href="{{Route('task.edit', ['task' => $task->id])}}" 
    class="btn">
        Edit
    </a>

    <form action="{{Route('tasks.destroy',['task' => $task->id])}}" method="POST">
        @csrf    
        @method('DELETE')
        <button type="submit" class="btn">Delete</button>
    </form>
</div>
@endsection